from django.db import models

# Create your models here.
class FAQ(models.Model):
    question_ua = models.CharField(max_length=300, verbose_name='Питання (UA)')
    answer_ua = models.TextField(verbose_name='Відповідь (UA)')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order']

    def __str__(self):
        return self.question_ua


class Partner(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')
    description_ua = models.CharField(max_length=300, blank=True, verbose_name='Опис (UA)')
    logo = models.ImageField(upload_to='partners/', blank=True, null=True, verbose_name='Логотип')
    website = models.URLField(blank=True, verbose_name='Сайт')
    instagram = models.URLField(blank=True, verbose_name='Instagram')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активно')


    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнери'
        ordering = ['order']


    def __str__(self):
        return self.name


class PricePackage(models.Model):
    name_ua = models.CharField(max_length=100, verbose_name='Назва (UA)')
    price_from = models.DecimalField(max_digits=8, decimal_places=0, verbose_name='Ціна від (€)')
    price_to = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True, verbose_name='Ціна до (€)')
    guests_ua = models.CharField(max_length=100, verbose_name='Гості (UA)')
    features_ua = models.TextField(verbose_name='Що входить (UA)', help_text='Кожен пункт з нового рядка')
    is_featured = models.BooleanField(default=False, verbose_name='Виділений (зірочка)')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активно')


    class Meta:
        verbose_name = 'Пакет прайсу'
        verbose_name_plural = 'Пакети прайсу'
        ordering = ['order']


    def __str__(self):
        return self.name_ua
