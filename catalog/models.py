# catalog/models.py

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class CatalogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def in_stock(self):
        return self.get_queryset().filter(stock__gt=0)

    def by_category(self, category):
        return self.get_queryset().filter(category=category)

    def price_range(self, min_price, max_price):
        return self.get_queryset().filter(price__gte=min_price, price__lte=max_price)

class Catalog(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    category = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CatalogManager()

    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def update_stock(self, quantity):
        if self.stock + quantity < 0:
            raise ValueError("Stock cannot be negative")
        self.stock += quantity
        self.save()

    def apply_discount(self, percentage):
        if not 0 <= percentage <= 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        discounted_price = self.price * (1 - percentage / 100)
        return round(discounted_price, 2)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving Catalog item {self.name}: {str(e)}")
            raise