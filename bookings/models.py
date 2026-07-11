from django.db import models


class BaseRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нова'),
        ('in_progress', 'В обробці'),
        ('confirmed', 'Підтверджена'),
        ('rejected', 'Відхилена'),
    ]

    name = models.CharField(max_length=200, verbose_name='Імʼя')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', blank=True, null=True)
    telegram = models.CharField(max_length=100, verbose_name='Telegram', blank=True, null=True)
    message = models.TextField(verbose_name='Повідомлення', blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус',
    )
    admin_notes = models.TextField(verbose_name='Нотатки', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.created_at.strftime("%d.%m.%Y")}'


class BookingRequest(BaseRequest):
    category = models.ForeignKey(
        'events.Category',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Категорія'
    )
    guests = models.PositiveIntegerField(verbose_name='Кількість гостей', blank=True, null=True)
    budget = models.CharField(max_length=100, verbose_name='Бюджет', blank=True, null=True)

    class Meta(BaseRequest.Meta):
        verbose_name = 'Заявка на бронювання'
        verbose_name_plural = 'Заявки на бронювання'


class PartnershipRequest(BaseRequest):
    TYPE_CHOICES = [
        ('location', 'Локація'),
        ('sponsor', 'Бренд / спонсор'),
        ('artist', 'Артист / MC'),
        ('other', 'Інше'),
    ]

    partnership_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        blank=True,
        verbose_name='Тип співпраці',
    )

    class Meta(BaseRequest.Meta):
        verbose_name = 'Заявка на партнерство'
        verbose_name_plural = 'Заявки на партнерство'