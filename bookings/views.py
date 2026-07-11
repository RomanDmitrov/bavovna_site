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

# Create your views here.
@throttle_post('booking', seconds=60)
def booking_create(request):
    if request.method == 'POST':
        form = BookingRequestForm(request.POST)

        if form.is_valid():
            booking = form.save()
            category_name = booking.category.name_ua if booking.category else '-'

            try:
                # noinspection PyTypeChecker
                resend.Emails.send({
                    "from": "onboarding@resend.dev",
                    "to": [settings.ADMIN_NOTIFICATION_EMAIL],
                    "subject": f"Нова заявка на бронювання — {html.escape(booking.name)}",
                    "html": (
                        f"<p><strong>Ім'я:</strong> {html.escape(booking.name)}</p>"
                        f"<p><strong>Email:</strong> {html.escape(booking.email or '-')}</p>"
                        f"<p><strong>Телефон:</strong> {html.escape(booking.phone or '-')}</p>"
                        f"<p><strong>Telegram:</strong> {html.escape(booking.telegram or '-')}</p>"
                        f"<p><strong>Тип івенту:</strong> {html.escape(category_name)}</p>"
                        f"<p><strong>Кількість гостей:</strong> {booking.guests or '-'}</p>"
                        f"<p><strong>Бюджет:</strong> {html.escape(booking.budget or '-')}</p>"
                        f"<p><strong>Повідомлення:</strong> {html.escape(booking.message or '-')}</p>"
                    ),
                })
            except Exception as e:
                logger.error(f"Failed to send email: {e}")

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

            try:
                # noinspection PyTypeChecker
                resend.Emails.send({
                    "from": "onboarding@resend.dev",
                    "to": [settings.ADMIN_NOTIFICATION_EMAIL],
                    "subject": f"Нова заявка на партнерство — {html.escape(partner_request.name)}",
                    "html": (
                        f"<p><strong>Ім'я / компанія:</strong> {html.escape(partner_request.name)}</p>"
                        f"<p><strong>Email:</strong> {html.escape(partner_request.email or '-')}</p>"
                        f"<p><strong>Телефон:</strong> {html.escape(partner_request.phone or '-')}</p>"
                        f"<p><strong>Telegram:</strong> {html.escape(partner_request.telegram or '-')}</p>"
                        f"<p><strong>Тип співпраці:</strong> {html.escape(partner_request.partnership_type or '-')}</p>"
                        f"<p><strong>Повідомлення:</strong> {html.escape(partner_request.message or '-')}</p>"
                    ),
                })
            except Exception as e:
                logger.error(f"Failed to send email: {e}")

            return redirect('booking_success')

        return render(request, 'bookings/partnership.html', {'form': form})

    return render(request, 'bookings/partnership.html')

