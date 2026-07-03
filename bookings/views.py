from django.shortcuts import render, redirect
from django.conf import settings
import resend
from .models import BookingRequest, PartnershipRequest
from pages.models import PricePackage

# Create your views here.
def booking_create(request):
    if request.method == 'POST':
        # Берём данные из формы которую отправил пользователь
        name = request.POST.get('name')
        email = request.POST.get('email') or None
        phone = request.POST.get('phone', '')
        telegram = request.POST.get('telegram', '')
        event_type = request.POST.get('event_type', '')
        guests = request.POST.get('guests')
        budget = request.POST.get('budget', '')
        message = request.POST.get('message', '')

        # Создаём запись в БД
        BookingRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            telegram=telegram,
            event_type=event_type,
            guests=guests if guests else None,
            budget=budget,
            message=message,
        )


        # Отправляем уведомление на почту
        try:
            # noinspection PyTypeChecker
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": [settings.ADMIN_NOTIFICATION_EMAIL],
                "subject": f"Нова заявка на бронювання — {name}",
                "html": (
                    f"<p><strong>Ім'я:</strong> {name}</p>"
                    f"<p><strong>Email:</strong> {email or '-'}</p>"
                    f"<p><strong>Телефон:</strong> {phone or '-'}</p>"
                    f"<p><strong>Telegram:</strong> {telegram or '-'}</p>"
                    f"<p><strong>Тип івенту:</strong> {event_type or '-'}</p>"
                    f"<p><strong>Кількість гостей:</strong> {guests or '-'}</p>"
                    f"<p><strong>Бюджет:</strong> {budget or '-'}</p>"
                    f"<p><strong>Повідомлення:</strong> {message or '-'}</p>"
                ),
            })
        except Exception as e:
            print(f"[EMAIL ERROR] {e}")

        # Перенаправляем на страницу успеха
        return redirect('booking_success')

    packages = PricePackage.objects.all().order_by('price_from')
    return render(request, 'bookings/booking.html', {'packages': packages})


def booking_success(request):
    return render(request, 'bookings/booking_success.html')


def partnership(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email') or None
        phone = request.POST.get('phone', '')
        telegram = request.POST.get('telegram', '')
        partnership_type = request.POST.get('partnership_type', '')
        message = request.POST.get('message', '')

        PartnershipRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            telegram=telegram,
            partnership_type=partnership_type,
            message=message,
        )


        # Отправляем уведомление на почту
        try:
            # noinspection PyTypeChecker
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": [settings.ADMIN_NOTIFICATION_EMAIL],
                "subject": f"Нова заявка на партнерство — {name}",
                "html": (
                    f"<p><strong>Ім'я / компанія:</strong> {name}</p>"
                    f"<p><strong>Email:</strong> {email or '-'}</p>"
                    f"<p><strong>Телефон:</strong> {phone or '-'}</p>"
                    f"<p><strong>Telegram:</strong> {telegram or '-'}</p>"
                    f"<p><strong>Тип співпраці:</strong> {partnership_type or '-'}</p>"
                    f"<p><strong>Повідомлення:</strong> {message or '-'}</p>"
                ),
            })
        except Exception as e:
            print(f"[EMAIL ERROR] {e}")

        return redirect('booking_success')

    return render(request, 'bookings/partnership.html')

