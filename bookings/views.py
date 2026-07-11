from django.shortcuts import render, redirect
from django.conf import settings
import resend
from .models import BookingRequest, PartnershipRequest
from events.models import Category
from config.ratelimit import throttle_post
from .forms import BookingRequestForm, PartnershipRequestForm
import logging
import html

logger = logging.getLogger(__name__)

def send_admin_email(subject, fields):
    html_body = ''.join(
        f"<p><strong>{label}:</strong> {html.escape(str(value)) if value else '-'}</p>"
        for label, value in fields
    )
    try:
        # noinspection PyTypeChecker
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": [settings.ADMIN_NOTIFICATION_EMAIL],
            "subject": subject,
            "html": html_body,
        })
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

# Create your views here.
@throttle_post('booking', seconds=60)
def booking_create(request):
    if request.method == 'POST':
        form = BookingRequestForm(request.POST)

        if form.is_valid():
            booking = form.save()
            category_name = booking.category.name_ua if booking.category else '-'

            send_admin_email(
                subject=f"Нова заявка на бронювання — {booking.name}",
                fields=[
                    ("Ім'я", booking.name),
                    ("Email", booking.email),
                    ("Телефон", booking.phone),
                    ("Telegram", booking.telegram),
                    ("Тип івенту", category_name),
                    ("Кількість гостей", booking.guests),
                    ("Бюджет", booking.budget),
                    ("Повідомлення", booking.message),
                ]
            )

            return redirect('booking_success')

        categories = Category.objects.filter(is_active=True)
        return render(request, 'bookings/booking.html', {'categories': categories, 'form': form})

    categories = Category.objects.filter(is_active=True)
    return render(request, 'bookings/booking.html', {'categories': categories})


def booking_success(request):
    return render(request, 'bookings/booking_success.html')

@throttle_post('partnership', seconds=60)
def partnership(request):
    if request.method == 'POST':
        form = PartnershipRequestForm(request.POST)

        if form.is_valid():
            partner_request = form.save()

            send_admin_email(
                subject=f"Нова заявка на партнерство — {partner_request.name}",
                fields=[
                    ("Ім'я / компанія", partner_request.name),
                    ("Email", partner_request.email),
                    ("Телефон", partner_request.phone),
                    ("Telegram", partner_request.telegram),
                    ("Тип співпраці", partner_request.partnership_type),
                    ("Повідомлення", partner_request.message),
                ]
            )

            return redirect('booking_success')

        return render(request, 'bookings/partnership.html', {'form': form})

    return render(request, 'bookings/partnership.html')

