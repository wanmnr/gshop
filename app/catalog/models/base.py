# models/base.py
from django.db import models
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving {self.__class__.__name__}: {str(e)}")
            raise