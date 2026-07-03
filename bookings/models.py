from django.db import models

# Create your models here.
class BookingRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нова'),
        ('in_progress', 'В обробці'),
        ('confirmed', 'Підтверджена'),
        ('rejected', 'Відхилена'),
    ]


    # Контакт инфо
    name = models.CharField(max_length=200, verbose_name='Імʼя')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', blank=True)
    telegram = models.CharField(max_length=100, verbose_name='Telegram', blank=True)


    # Детали ивента
    event_type = models.CharField(max_length=200, verbose_name='Тип івенту', blank=True)
    guests = models.PositiveIntegerField(verbose_name='Кількість гостей', blank=True, null=True)
    budget = models.CharField(max_length=100, verbose_name='Бюджет', blank=True)
    message = models.TextField(verbose_name='Повідомлення', blank=True)


    # Статус Заявки
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус',
    )


    # Заметки для организаторов
    admin_notes = models.TextField(verbose_name='Нотатки', blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заявка на бронювання'
        verbose_name_plural = 'Заявки на бронювання'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.created_at.strftime("%d.%m.%Y")}'




class PartnershipRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нова'),
        ('in_progress', 'В обробці'),
        ('confirmed', 'Підтверджена'),
        ('rejected', 'Відхилена'),
    ]

    TYPE_CHOICES = [
        ('location', 'Локація'),
        ('sponsor', 'Бренд / спонсор'),
        ('artist', 'Артист / MC'),
        ('other', 'Інше'),
    ]

    # Контакт інфо
    name = models.CharField(max_length=200, verbose_name='Імʼя / компанія')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', blank=True, null=True)
    telegram = models.CharField(max_length=100, verbose_name='Telegram', blank=True, null=True)

    # Деталі співпраці
    partnership_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        blank=True,
        verbose_name='Тип співпраці',
    )
    message = models.TextField(verbose_name='Повідомлення', blank=True)

    # Статус заявки
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус',
    )

    # Нотатки для організаторів
    admin_notes = models.TextField(verbose_name='Нотатки', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заявка на партнерство'
        verbose_name_plural = 'Заявки на партнерство'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.created_at.strftime("%d.%m.%Y")}'