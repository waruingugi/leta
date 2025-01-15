from decimal import Decimal

from django.db import models
from django.utils.timezone import now

from commons.constants import DiscountType, OrderStatus
from commons.models import Base
from products.models import Product
from users.models import Customer


class Discount(Base):
    """Discount Model"""

    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10,
        choices=[(type.value, type.value) for type in DiscountType],
        default=DiscountType.FLAT.value,
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"
        ordering = ("-valid_from",)

    def __str__(self) -> str:
        return f"{self.name} ({self.type.capitalize()}: {self.value})"

    def is_active(self) -> bool:
        """Check if the discount is currently active."""
        return self.valid_from <= now() <= self.valid_until


class Order(Base):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(
        max_length=10,
        choices=[(status.value, status.value) for status in OrderStatus],
        default=OrderStatus.PENDING.value,
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    discount_applied = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Order #{self.id} - {self.customer.user.name}"

    def calculate_total_price(self):
        """Recalculate total_price based on associated OrderItems."""
        total = sum(item.price * item.quantity for item in self.order_items.all())
        if self.discount_applied:
            total -= total * (self.discount_applied / Decimal("100"))
        self.total_price = total
        self.save()


class OrderItem(Base):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"

    def save(self, *args, **kwargs):
        """
        Automatically set the price based on the product's price
        when the OrderItem is created or updated.
        """
        if not self.pk:  # Only set price on first save
            self.price = self.product.price
        super().save(*args, **kwargs)

    def total_price(self) -> float:
        """Calculate the total price for this order item."""
        return float(self.price) * self.quantity
