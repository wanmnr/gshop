# models/catalog.py
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from .base import BaseModel

class Catalog(BaseModel):
    class CategoryChoices(models.TextChoices):
        ELECTRONICS = 'ELECTRONICS', _('Electronics')
        CLOTHING = 'CLOTHING', _('Clothing')
        BOOKS = 'BOOKS', _('Books')
        FOOD = 'FOOD', _('Food')
        OTHER = 'OTHER', _('Other')

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Product name")
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text=_("Product description")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text=_("Product price")
    )
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        help_text=_("Product category")
    )
    stock = models.PositiveIntegerField(
        default=0,
        help_text=_("Available stock")
    )

    class Meta:
        verbose_name = _("Catalog Item")
        verbose_name_plural = _("Catalog Items")
        indexes = [
            models.Index(fields=['category'], name='idx_catalog_category'),
            models.Index(fields=['price'], name='idx_catalog_price'),
        ]
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.category})"

    def is_in_stock(self):
        return self.stock > 0

    def update_stock(self, quantity):
        if self.stock + quantity < 0:
            raise ValueError(_("Stock cannot be negative"))
        self.stock += quantity
        self.save()