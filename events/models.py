from django.db import models

# Create your models here.
class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('regular', 'Звичайний івент'),
        ('community', 'Community івент'),
    ]


    title_ua = models.CharField(max_length= 200, verbose_name= 'Назва (UA)')
    title_en = models.CharField(max_length= 200, verbose_name= 'Title (EN)')
    event_type = models.CharField(
        max_length = 20,
        choices = EVENT_TYPE_CHOICES,
        default = 'regular',
        verbose_name = 'Тип івенту'
    )


    date = models.DateTimeField(verbose_name= 'Дата та час')
    venue_ua = models.CharField(max_length= 300, verbose_name= 'Місце (UA)')
    venue_en = models.CharField(max_length= 300, verbose_name= 'Venue (EN)')


    description_ua = models.TextField(verbose_name= 'Опис (UA)')
    description_en = models.TextField(verbose_name= 'Description (EN)')


    cover_image = models.ImageField(
        upload_to = 'events/covers/',
        verbose_name = 'Обкладинка',
        blank = True,
        null = True
    )


    ticket_price = models.DecimalField(
        max_digits = 8,
        decimal_places = 2,
        verbose_name = 'Ціна квитка (€)',
        blank = True,
        null = True
    )
    ticket_limit = models.PositiveIntegerField(
        verbose_name = 'Ліміт місць',
        blank = True,
        null = True
    )
    ticket_url = models.URLField(
        verbose_name = 'Посилання на квитки',
        blank = True
    )
    photo_album_url = models.URLField(
        verbose_name='Посилання на фотоальбом (Google Drive)',
        blank=True
    )
    is_published = models.BooleanField(
        default = False,
        verbose_name = 'Опубліковано'
    )


    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    class Meta:
        verbose_name = 'Івент'
        verbose_name_plural = 'Івенти'
        ordering = ['-date']

    def __str__(self):
        return self.title_ua


class GalleryItem(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='gallery',
        verbose_name='Івент'
    )
    image = models.ImageField(
        upload_to = 'events/gallery/',
        verbose_name = 'Фото (завантажити)',
        blank = True,
        null = True
    )

    created_at = models.DateTimeField(auto_now_add = True)


    class Meta:
        verbose_name = 'Фото галереї'
        verbose_name_plural = 'Фото галереї'
        ordering = ['created_at']


    def __str__(self):
        return f'{self.event.title_ua} - фото {self.id}'


