# from multiprocessing.managers import public_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Event, Category
from pages.models import FAQ
import boto3
import uuid
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from config.ratelimit import throttle_post
from comments.forms import CommentForm

# Create your views here.
def event_list(request):
    category_slug = request.GET.get('category')

    # Все опубликованые будущие ивенты
    upcoming_events = Event.objects.filter(
        is_published=True,
        date__gte=timezone.now()
    ).select_related('category').order_by('date')

    if category_slug:
        upcoming_events = upcoming_events.filter(category__slug=category_slug)

    upcoming_event = upcoming_events.first()
    future_events = upcoming_events[1:] if upcoming_event else []

    categories = Category.objects.filter(is_active=True)


    context = {
        'upcoming_event': upcoming_event,
        'future_events': future_events,
        'categories': categories,
        'selected_category': category_slug,
    }

    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    # Берём конкретный ивент по ID или возвращаем 404
    event = get_object_or_404(Event, pk=pk, is_published=True)
    comments = event.comments.filter(is_approved=True)
    faqs = FAQ.objects.filter(is_active=True).filter(
    Q(show_on_all_events=True) | Q(events=event)
    )
    is_past = event.date < timezone.now()
    photo_album_url = event.photo_album_url



    context = {
        'event': event,
        'comments': comments,
        'faqs': faqs,
        'is_past': is_past,
        'photo_album_url': photo_album_url,
    }
    return render(request, 'events/event_detail.html', context)


def gallery(request):
    category_slug = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    events = Event.objects.filter(
        is_published=True,
        date__lt=timezone.now()
    ).select_related('category').exclude(photo_album_url='').order_by('-date')

    if category_slug:
        events = events.filter(category__slug=category_slug)

    if date_from:
        events = events.filter(date__gte=date_from)

    if date_to:
        events = events.filter(date__lte=date_to)

    categories = Category.objects.filter(is_active=True)

    context = {
        'events': events,
        'categories': categories,
        'selected_category': category_slug,
        'date_from': date_from,
        'date_to': date_to,
    }

    return render(request, 'events/gallery.html', context)


@throttle_post('comment', seconds=30)
def comment_add(request, pk):
    event = get_object_or_404(Event, pk=pk, is_published=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.save()

    return redirect('event_comments', pk=pk)


def event_comments(request, pk):
    event = get_object_or_404(Event, pk=pk, is_published=True)
    comments = event.comments.filter(is_approved=True).order_by('-created_at')

    context = {
        'event': event,
        'comments': comments,
    }
    return render(request, 'events/event_comments.html', context)


@staff_member_required
@require_GET
def get_presigned_upload_url(request):
    """
        Генерирует подписанный URL для прямой загрузки файла в R2.
        Только для сотрудников (staff) - используется в админке.
    """
    ALLOWED_CONTENT_TYPES = {
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'image/webp': 'webp',
        'image/gif': 'gif',
    }

    content_type = request.GET.get('content_type', 'image/jpeg')

    if content_type not in ALLOWED_CONTENT_TYPES:
        return JsonResponse({'error': 'Непідтримуваний тип файлу'}, status=400)

    ext = ALLOWED_CONTENT_TYPES[content_type]
    unique_key = f'events/gallery/{uuid.uuid4()}.{ext}'

    client = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='auto',
    )

    presigned_url = client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': unique_key,
            'ContentType': content_type,
            'ContentLengthRange': (0, 10 * 1024 * 1024),
        },
        ExpiresIn=300,
    )

    public_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_key}'

    return JsonResponse({
        'upload_url': presigned_url,
        'key': unique_key,
        'public_url': public_url,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    events = category.events.filter(
        is_published=True,
        date__gte=timezone.now()
    ).order_by('date')

    context = {
        'category': category,
        'events': events,
    }
    return render(request, f'events/categories/{slug}.html', context)