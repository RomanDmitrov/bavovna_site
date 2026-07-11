import requests
import logging
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookingRequest, PartnershipRequest

logger = logging.getLogger(__name__)

NOTIFIER_URL = os.getenv('NOTIFIER_URL', "https://web-production-8ae9b.up.railway.app/notify")


def send_notification(request_type, payload):
    payload['request_type'] = request_type
    try:
        requests.post(NOTIFIER_URL, json=payload, timeout=5)
    except requests.RequestException as e:
        logger.error(f"Failed to send {request_type} notification: {e}")


@receiver(post_save, sender=BookingRequest)
def notify_new_booking(sender, instance, created, **kwargs):
    if not created:
        return

    send_notification('booking', {
        "name": instance.name,
        "email": instance.email,
        "phone": instance.phone,
        "telegram": instance.telegram,
        "category": instance.category.name_ua if instance.category else None,
        "guests": instance.guests,
        "budget": instance.budget,
        "message": instance.message,
    })


@receiver(post_save, sender=PartnershipRequest)
def notify_new_partnership(sender, instance, created, **kwargs):
    if not created:
        return

    send_notification('partnership', {
        "name": instance.name,
        "email": instance.email,
        "phone": instance.phone,
        "telegram": instance.telegram,
        "partnership_type": instance.partnership_type,
        "message": instance.message,
    })