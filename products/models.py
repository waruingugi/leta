from django.db import models

from commons.constants import SUPPLIER_SHARE
from commons.models import Base


class Category(Base):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class Supplier(Base):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class Product(Base):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )
    reorder_threshold = models.PositiveIntegerField(default=10)
    supplier = models.ForeignKey(
        "Supplier",
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("-created_at",)

    def needs_reorder(self) -> bool:
        """Check if the product stock is below the reorder threshold."""
        return self.stock_quantity < self.reorder_threshold

    def supplier_share(self) -> float:
        """Total cut of revenue for supplier."""
        return float(self.price) * SUPPLIER_SHARE

    def __str__(self) -> str:
        return self.name
