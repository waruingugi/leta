from decimal import Decimal

from django.urls import reverse
from rest_framework import status

from commons.tests.base import UserBaseAPITestCase
from products.models import Category, Product


class CategoryViewTests(UserBaseAPITestCase):
    def setUp(self) -> None:
        # Create parent category
        self.parent_category = Category.objects.create(name="Electronics")

        # Create subcategory
        self.subcategory = Category.objects.create(
            name="Laptops", parent=self.parent_category
        )

        # Create products
        self.product1 = Product.objects.create(
            name="Gaming Laptop",
            description="High-performance laptop for gaming.",
            price=Decimal("1500.00"),
            stock_quantity=20,
            category=self.subcategory,
            is_active=True,
        )
        self.product2 = Product.objects.create(
            name="Business Laptop",
            description="Efficient laptop for business use.",
            price=Decimal("1200.00"),
            stock_quantity=15,
            category=self.subcategory,
            is_active=True,
        )
        self.force_authenticate_staff_user()

        # URLs
        self.create_url = reverse("categories:create")
        self.list_url = reverse("categories:list")
        self.detail_url = reverse(
            "categories:detail", kwargs={"id": self.parent_category.id}
        )
        self.nested_url = reverse(
            "categories:nested-products", kwargs={"id": self.parent_category.id}
        )

    def test_create_category(self) -> None:
        """Test creating a new category."""
        data = {"name": "Smartphones", "parent": self.parent_category.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(name="Smartphones").count(), 1)

    def test_list_categories(self) -> None:
        """Test listing all top-level categories."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Electronics")

    def test_retrieve_category(self) -> None:
        """Test retrieving a specific category."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Electronics")
        self.assertEqual(len(response.data["subcategories"]), 1)

    def test_update_category(self) -> None:
        """Test updating a specific category."""
        data = {"name": "Updated Electronics"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.parent_category.refresh_from_db()
        self.assertEqual(self.parent_category.name, "Updated Electronics")

    def test_nested_category_products(self) -> None:
        """Test fetching all products in a category, including nested subcategories."""
        response = self.client.get(self.nested_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Electronics")
        self.assertEqual(len(response.data["subcategories"]), 1)
        self.assertEqual(len(response.data["subcategories"][0]["products"]), 2)
