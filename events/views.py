from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Event
from pages.models import FAQ
from comments.models import Comment

# Create your views here.
def event_list(request):
    # Все опубликованые будущие ивенты
    upcoming_event = Event.objects.filter(
        is_published=True,
        event_type='regular',
        date__gte=timezone.now()
    ).order_by('date').first()

    context = {
        'upcoming_event': upcoming_event,
    }

    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    # Берём конкретный ивент по ID или возвращаем 404
    event = get_object_or_404(Event, pk=pk, is_published=True)
    comments = event.comments.filter(is_approved=True)
    faqs = FAQ.objects.filter(is_active=True)

    context = {
        'event': event,
        'comments': comments,
        'faqs': faqs,
    }
    return render(request, 'events/event_detail.html', context)


def gallery(request):
    events = Event.objects.filter(
        is_published=True,
        date__lt=timezone.now()
    ).order_by('-date')

    context = {
        'events': events,
    }

    return render(request, 'events/gallery.html', context)


def comment_add(request, pk):
    event = get_object_or_404(Event, pk=pk, is_published=True)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        text = request.POST.get('text', '').strip()

        if name and text:
            Comment.objects.create(
                event=event,
                name=name,
                text=text,
                is_approved=True
            )

    return redirect('event_detail', pk=pk)