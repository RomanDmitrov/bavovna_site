import requests
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookingRequest, PartnershipRequest
import os

logger = logging.getLogger(__name__)

NOTIFIER_URL = os.getenv('NOTIFIER_URL', "https://web-production-8ae9b.up.railway.app/notify")


@receiver(post_save, sender=BookingRequest)
def notify_new_booking(sender, instance, created, **kwargs):
    if not created:
        return

    payload = {
        "request_type": "booking",
        "name": instance.name,
        "email": instance.email,
        "phone": instance.phone,
        "telegram": instance.telegram,
        "category": instance.category.name_ua if instance.category else None,
        "guests": instance.guests,
        "budget": instance.budget,
        "message": instance.message,
    }

    try:
        requests.post(NOTIFIER_URL, json=payload, timeout=5)
    except requests.RequestException as e:
        logger.error(f"Failed to send booking notification: {e}")


@receiver(post_save, sender=PartnershipRequest)
def notify_new_partnership(sender, instance, created, **kwargs):
    if not created:
        return

    payload = {
        "request_type": "partnership",
        "name": instance.name,
        "email": instance.email,
        "phone": instance.phone,
        "telegram": instance.telegram,
        "partnership_type": instance.partnership_type,
        "message": instance.message,
    }

    try:
        requests.post(NOTIFIER_URL, json=payload, timeout=5)
    except requests.RequestException as e:
        logger.error(f"Failed to send partnership notification: {e}")
