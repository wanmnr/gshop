# accounts/models.py

import logging
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils import timezone

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Account(models.Model):
    username = models.CharField(
        max_length=50, 
        unique=True, 
        validators=[MinLengthValidator(3)],
        error_messages={
            'unique': "This username is already taken.",
        }
    )
    email = models.EmailField(
        max_length=100, 
        unique=True,
        error_messages={
            'unique': "An account with this email already exists.",
        }
    )
    password = models.CharField(
        max_length=255
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(
        max_length=15, 
        null=True, 
        blank=True, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        try:
            self.updated_at = timezone.now()
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving Account: {str(e)}")
            raise

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        indexes = [
            models.Index(fields=['email'], name='idx_accounts_email'),
        ]
