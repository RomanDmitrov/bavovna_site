from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
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
        send_mail(
            subject=f'Нова заявка на бронювання — {name}',
            message=(
                f"Ім'я: {name}\n"
                f"Email: {email or '-'}\n"
                f"Телефон: {phone or '-'}\n"
                f"Telegram: {telegram or '-'}\n"
                f"Тип івенту: {event_type or '-'}\n"
                f"Кількість гостей: {guests or '-'}\n"
                f"Бюджет: {budget or '-'}\n"
                f"Повідомлення: {message or '-'}\n"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
            fail_silently=True,
        )

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
        send_mail(
            subject=f'Нова заявка на партнерство — {name}',
            message=(
                f"Ім'я / компанія: {name}\n"
                f"Email: {email or '-'}\n"
                f"Телефон: {phone or '-'}\n"
                f"Telegram: {telegram or '-'}\n"
                f"Тип співпраці: {partnership_type or '-'}\n"
                f"Повідомлення: {message or '-'}\n"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
            fail_silently=True,
        )

        return redirect('booking_success')

    return render(request, 'bookings/partnership.html')

