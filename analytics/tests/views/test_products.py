from decimal import Decimal

from django.urls import reverse
from rest_framework import status

from commons.constants import MembershipLevel
from commons.tests.base import UserBaseAPITestCase
from orders.models import Order, OrderItem
from products.models import Product
from users.models import Customer


class BestSellingProductsViewTests(UserBaseAPITestCase):
    def setUp(self) -> None:
        self.user = self.create_user()
        self.customer = Customer.objects.create(
            user=self.user, membership=MembershipLevel.BRONZE.value
        )
        # Create sample products
        self.product1 = Product.objects.create(
            name="Laptop", price=Decimal("1000.00"), stock_quantity=50
        )
        self.product2 = Product.objects.create(
            name="Smartphone", price=Decimal("500.00"), stock_quantity=100
        )

        # Create an order and add items
        self.order = Order.objects.create(customer=self.customer)
        OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            quantity=150,
            price=self.product1.price,
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            quantity=120,
            price=self.product2.price,
        )

        # URL for the best-selling products endpoint
        self.url = reverse("analytics:best-selling-products")
        self.force_authenticate_staff_user()

    def test_best_selling_products_default_limit(self) -> None:
        """Test retrieving the default number of best-selling products."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 2
        )  # Default limit should include all products

    def test_best_selling_products_with_limit(self) -> None:
        """Test retrieving a limited number of best-selling products."""
        response = self.client.get(self.url, {"limit": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Laptop")
        self.assertEqual(response.data[0]["total_sold"], 150)

    def test_best_selling_products_no_sales(self) -> None:
        """Test response when there are no sales."""
        OrderItem.objects.all().delete()  # Remove all sales data
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
