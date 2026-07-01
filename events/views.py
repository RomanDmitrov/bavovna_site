# from multiprocessing.managers import public_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Event
from pages.models import FAQ
from comments.models import Comment
import boto3
import uuid
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET

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


@staff_member_required
@require_GET
def get_presigned_upload_url(request):
    """
        Генерирует подписанный URL для прямой загрузки файла в R2.
        Только для сотрудников (staff) - используется в админке.
    """
    original_filename = request.GET.get('filename', 'file.jpg')
    content_type = request.GET.get('content_type', 'image/jpeg')

    ext = original_filename.split('.')[-1] if '.' in original_filename else 'jpg'
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
        },
        ExpiresIn=300,
    )

    public_url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_key}'

    return JsonResponse({
        'upload_url': presigned_url,
        'key': unique_key,
        'public_url': public_url,

    })