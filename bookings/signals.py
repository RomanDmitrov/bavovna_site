import requests
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookingRequest, PartnershipRequest

logger = logging.getLogger(__name__)

NOTIFIER_URL = "http://127.0.0.1:8000/notify"


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
        "event_type": instance.event_type,
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
