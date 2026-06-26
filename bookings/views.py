from django.shortcuts import render, redirect
from .models import BookingRequest
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

        # Перенаправляем на страницу успеха
        return redirect('booking_success')

    packages = PricePackage.objects.all().order_by('price')
    return render(request, 'bookings/booking.html', {'packages': packages})


def booking_success(request):
    return render(request, 'bookings/booking_success.html')


def partnership(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact', '')
        message = request.POST.get('message', '')

        BookingRequest.objects.create(
            name=name,
            email=contact,
            message=message,
            event_type='partnership'
        )
        return redirect('booking_success')

    return render(request, 'bookings/partnership.html')

