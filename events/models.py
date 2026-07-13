from django.db import models
from config.image_utils import compress_image_field

# Create your models here.
class Event(models.Model):

    def save(self, *args, **kwargs):
        compress_image_field(self.cover_image)
        super().save(*args, **kwargs)

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='events',
        verbose_name='Категорія'
    )


    title_ua = models.CharField(max_length= 200, verbose_name= 'Назва (UA)')
    title_en = models.CharField(max_length= 200, verbose_name= 'Title (EN)')


    date = models.DateTimeField(verbose_name= 'Дата та час', db_index=True)
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
        default=False,
        verbose_name='Опубліковано',
        db_index=True
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

    def save(self, *args, **kwargs):
        if hasattr(self, '_r2_key') and self._r2_key:
            self.image.name = self._r2_key
        super().save(*args, **kwargs)

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


class Category(models.Model):
    name_ua = models.CharField(max_length=100, verbose_name='Назва (UA)')
    name_en = models.CharField(max_length=100, verbose_name='Name (EN)')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug (для URL)')
    icon = models.CharField(max_length=10, blank=True, verbose_name='Емодзі-іконка')
    description_ua = models.CharField(max_length=160, blank=True, verbose_name='Короткий опис (UA)')
    description_en = models.CharField(max_length=160, blank=True, verbose_name='Short description (EN)')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['order']

    def __str__(self):
        return self.name_ua