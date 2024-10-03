# models.py

from django.db import models
from django.core.exceptions import ValidationError
import logging

# Configure logging
logger = logging.getLogger(__name__)

class UserType(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    CUSTOMER = 'customer', 'Customer'

class AccountStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'

class User(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for each user
    name = models.CharField(max_length=100)  # Full name of the user
    email = models.EmailField(unique=True)    # Unique email address for the user
    password = models.CharField(max_length=255)  # User's password
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    user_type = models.CharField(max_length=10, choices=UserType.choices)  # User type
    account_status = models.CharField(max_length=10, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)  # Account status
    date_joined = models.DateTimeField(auto_now_add=True)  # Date the user joined

    class Meta:
        indexes = [
            models.Index(fields=['email'], name='idx_email'),  # Index on email
            models.Index(fields=['user_type'], name='idx_user_type'),  # Index on user type
        ]

    def clean(self):
        if not self.email:
            logger.warning('Validation failed: Email cannot be empty.')
            raise ValidationError('Email cannot be empty.')
        if not self.password:
            logger.warning('Validation failed: Password cannot be empty.')
            raise ValidationError('Password cannot be empty.')

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        try:
            super().save(*args, **kwargs)  # Call the original save method
            logger.info(f'User {self.name} saved successfully.')
        except Exception as e:
            logger.error(f'Error saving user {self.name}: {e}')
            raise  # Re-raise the exception after logging

    def __str__(self):
        return f"{self.name} ({self.user_type})"