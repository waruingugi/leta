from decimal import Decimal
from unittest.mock import patch

from django.urls import reverse
from django.utils.timezone import now, timedelta
from rest_framework import status

from commons.constants import MembershipLevel, OrderStatus
from commons.tests.base import UserBaseAPITestCase
from orders.models import Order
from users.models import Customer


class TotalRevenueViewTests(UserBaseAPITestCase):
    def setUp(self):
        self.user = self.create_user()
        # Create a customer
        self.customer = Customer.objects.create(
            user=self.user, membership=MembershipLevel.BRONZE.value
        )

        # URL for the total revenue endpoint
        self.url = reverse("analytics:total-revenue")
        self.force_authenticate_staff_user()

    @patch("django.utils.timezone.now")
    def test_total_revenue_without_date_range(self, mock_now) -> None:
        """Test total revenue calculation without date range."""
        mock_now.return_value = now() - timedelta(days=5)
        Order.objects.bulk_create(
            [
                Order(
                    customer=self.customer,
                    status=OrderStatus.COMPLETED.value,
                    total_price=Decimal("100.50"),
                ),
                Order(
                    customer=self.customer,
                    status=OrderStatus.COMPLETED.value,
                    total_price=Decimal("200.75"),
                ),
                Order(
                    customer=self.customer,
                    status=OrderStatus.PENDING.value,
                    total_price=Decimal("300.25"),
                ),
            ]
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_revenue"], Decimal("301.25"))

    @patch("django.utils.timezone.now")
    def test_total_revenue_with_date_range(self, mock_now) -> None:
        """Test total revenue calculation with a date range."""
        mock_now.return_value = now() - timedelta(days=5)
        Order.objects.create(
            customer=self.customer,
            status=OrderStatus.COMPLETED.value,
            total_price=Decimal("100.50"),
        )

        mock_now.return_value = now() - timedelta(days=2)
        Order.objects.create(
            customer=self.customer,
            status=OrderStatus.COMPLETED.value,
            total_price=Decimal("200.75"),
        )

        start_date = (now() - timedelta(days=3)).date().isoformat()
        response = self.client.get(self.url, {"start_date": start_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_revenue"], Decimal("200.75"))

    @patch("django.utils.timezone.now")
    def test_total_revenue_with_invalid_date(self, mock_now) -> None:
        """Test total revenue calculation with invalid date format."""
        response = self.client.get(self.url, {"start_date": "invalid-date"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("start_date", response.data)

    @patch("django.utils.timezone.now")
    def test_total_revenue_with_end_date(self, mock_now) -> None:
        """Test total revenue calculation with only an end date."""
        mock_now.return_value = now() - timedelta(days=5)
        Order.objects.create(
            customer=self.customer,
            status=OrderStatus.COMPLETED.value,
            total_price=Decimal("100.50"),
        )

        mock_now.return_value = now() - timedelta(days=2)
        Order.objects.create(
            customer=self.customer,
            status=OrderStatus.COMPLETED.value,
            total_price=Decimal("200.75"),
        )

        end_date = (now() - timedelta(days=4)).date().isoformat()
        response = self.client.get(self.url, {"end_date": end_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_revenue"], Decimal("100.50"))

    @patch("django.utils.timezone.now")
    def test_total_revenue_with_start_and_end_date(self, mock_now) -> None:
        """Test total revenue calculation with both start and end dates."""
        mock_now.return_value = now() - timedelta(days=5)
        Order.objects.create(
            customer=self.customer,
            status=OrderStatus.COMPLETED.value,
            total_price=Decimal("100.50"),
        )

        mock_now.return_value = now() - timedelta(days=2)
        Order.objects.create(
            customer=self.customer,
            status=OrderStatus.COMPLETED.value,
            total_price=Decimal("200.75"),
        )

        start_date = (now() - timedelta(days=6)).date().isoformat()
        end_date = (now() - timedelta(days=4)).date().isoformat()
        response = self.client.get(
            self.url, {"start_date": start_date, "end_date": end_date}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_revenue"], Decimal("100.50"))
