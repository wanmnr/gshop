# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Account)
def log_account_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New account created: {instance.username}")