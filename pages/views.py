from django.shortcuts import render
from django.utils import timezone
from events.models import Event
from .models import Partner, FAQ, PricePackage


def home(request):
    # Ближайший будущий опубликованный ивент
    upcoming_event = Event.objects.filter(
        is_published=True,
        event_type='regular',
        date__gte=timezone.now()  # date >= текущее время
    ).order_by('date').first()
    # Последние 3 прошедших ивента для галереи
    past_events = Event.objects.filter(
        is_published=True,
        date__lt=timezone.now()  # date < текущее время
    ).order_by('-date')[:3]
    partners = Partner.objects.filter(is_active=True)
    packages = PricePackage.objects.filter(is_active=True)
    context = {
        'upcoming_event': upcoming_event,
        'past_events': past_events,
        'partners': partners,
        'packages': packages,
    }

    return render(request, 'pages/home.html', context)