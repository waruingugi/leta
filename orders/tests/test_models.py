from decimal import Decimal

from django.test import TestCase
from django.utils.timezone import now, timedelta

from orders.models import Discount, DiscountType


class DiscountModelTestCase(TestCase):
    def setUp(self) -> None:
        # Create active discount
        self.active_discount = Discount.objects.create(
            name="Active Discount",
            type=DiscountType.FLAT.value,
            value=Decimal("50.00"),
            valid_from=now() - timedelta(days=1),
            valid_until=now() + timedelta(days=1),
        )

        # Create expired discount
        self.expired_discount = Discount.objects.create(
            name="Expired Discount",
            type=DiscountType.FLAT.value,
            value=Decimal("30.00"),
            valid_from=now() - timedelta(days=10),
            valid_until=now() - timedelta(days=5),
        )

        # Create upcoming discount
        self.upcoming_discount = Discount.objects.create(
            name="Upcoming Discount",
            type=DiscountType.FLAT.value,
            value=Decimal("20.00"),
            valid_from=now() + timedelta(days=2),
            valid_until=now() + timedelta(days=7),
        )

    def test_discount_creation(self) -> None:
        """Test that discounts are created correctly."""
        self.assertEqual(self.active_discount.name, "Active Discount")
        self.assertEqual(self.active_discount.type, DiscountType.FLAT.value)
        self.assertEqual(self.active_discount.value, Decimal("50.00"))

    def test_is_active_method(self) -> None:
        """Test the is_active method."""
        # Active discount should return True
        self.assertTrue(self.active_discount.is_active())

        # Expired discount should return False
        self.assertFalse(self.expired_discount.is_active())

        # Upcoming discount should return False
        self.assertFalse(self.upcoming_discount.is_active())

    def test_discount_str(self) -> None:
        """Test the __str__ method."""
        self.assertEqual(str(self.active_discount), "Active Discount (Flat: 50.00)")
