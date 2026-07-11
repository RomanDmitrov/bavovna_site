from django.shortcuts import render, redirect
from django.utils import timezone
from events.models import Event, Category
from datetime import date
from .models import Partner

COMPANY_FOUNDED_DATE = date(2023, 12, 23)
PUBLIC_CATEGORY_SLUGS = ['concerts', 'club-shows', 'stand-up', 'activities', 'festivals']
def home(request):
    # Ближайший будущий ивент ЛЮБОЙ категории — для hero-блока
    upcoming_event = Event.objects.filter(
        is_published=True,
        date__gte=timezone.now()
    ).select_related('category').order_by('date').first()

    # Карусель "Останні події" — до 10 публичных ивентов
    upcoming_public_events = Event.objects.filter(
        is_published=True,
        date__gte=timezone.now(),
        category__slug__in=PUBLIC_CATEGORY_SLUGS
    ).select_related('category').order_by('date')[:10]

    upcoming_count = upcoming_public_events.count()

    if upcoming_count < 10:
        remaining_slots = 10 - upcoming_count
        past_public_events = Event.objects.filter(
            is_published=True,
            date__lt=timezone.now(),
            category__slug__in=PUBLIC_CATEGORY_SLUGS
        ).select_related('category').order_by('-date')[:remaining_slots]
        recent_public_events = list(upcoming_public_events) + list(past_public_events)
    else:
        recent_public_events = list(upcoming_public_events)


    # Последние 3 прошедших ивента для галереи


    past_events = Event.objects.filter(
        is_published=True,
        date__lt=timezone.now()  # date < текущее время
    ).select_related('category').order_by('-date')[:3]
    partners = Partner.objects.filter(is_active=True)

    events_count = Event.objects.filter(
        is_published=True,
        date__lt=timezone.now()
    ).count()

    years_on_market = (timezone.now().date() - COMPANY_FOUNDED_DATE).days // 365

    categories = Category.objects.filter(is_active=True)

    context = {
        'upcoming_event': upcoming_event,
        'upcoming_public_events': upcoming_public_events,
        'past_events': past_events,
        'partners': partners,
        'events_count': events_count,
        'years_on_market': years_on_market,
        'categories': categories,
        'recent_public_events': recent_public_events,
    }

    return render(request, 'pages/home.html', context)


def set_language(request, lang_code):
    if lang_code in ['ua', 'en']:
        request.session['language'] = lang_code

    # Возвращаем пользователя туда, откуда он пришёл
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)

def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'pages/terms_of_service.html')

def gdpr_policy(request):
    return render(request, 'pages/gdpr_policy.html')