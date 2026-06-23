from django.db import models
from events.models import Event

# Create your models here.
class Comment(models.Model):
    # Привязка к ивенту
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Івент'
    )


    name = models.CharField(max_length=100, verbose_name='Імʼя')
    text = models.TextField(verbose_name='Відгук')


    is_approved = models.BooleanField(
        default=True,
        verbose_name= 'Схвалено'
    )


    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-created_at']


    def __str__(self):
        return f'{self.name} - {self.event.title_ua}'