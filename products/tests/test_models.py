from decimal import Decimal

from django.test import TestCase

from commons.constants import SUPPLIER_SHARE
from products.models import Category, Product, Supplier


class CategoryModelTests(TestCase):
    def test_category_creation(self) -> None:
        """Test the creation of a category without parent."""
        category = Category.objects.create(name="Electronics")
        self.assertEqual(category.name, "Electronics")
        self.assertIsNone(category.parent)

    def test_category_creation_with_parent(self) -> None:
        """Test the creation of a category with a parent."""
        parent_category = Category.objects.create(name="Electronics")
        child_category = Category.objects.create(name="Laptops", parent=parent_category)

        self.assertEqual(child_category.name, "Laptops")
        self.assertEqual(child_category.parent, parent_category)

    def test_parent_child_relationship(self) -> None:
        """Test if subcategories can be retrieved using the related name."""
        parent_category = Category.objects.create(name="Electronics")
        subcategory_1 = Category.objects.create(name="Laptops", parent=parent_category)
        subcategory_2 = Category.objects.create(
            name="Smartphones", parent=parent_category
        )

        # Retrieve subcategories of 'Electronics'
        subcategories = parent_category.subcategories.all()

        self.assertEqual(subcategories.count(), 2)
        self.assertIn(subcategory_1, subcategories)
        self.assertIn(subcategory_2, subcategories)

    def test_category_str_method(self) -> None:
        """Test the string representation of the category."""
        category = Category.objects.create(name="Electronics")
        self.assertEqual(str(category), "Electronics")

    def test_top_level_category(self) -> None:
        """Test top-level category (without parent)."""
        category = Category.objects.create(name="Furniture")
        self.assertIsNone(category.parent)

    def test_subcategory_of_subcategory(self) -> None:
        """Test the subcategory of a subcategory."""
        parent_category = Category.objects.create(name="Electronics")
        subcategory_1 = Category.objects.create(name="Laptops", parent=parent_category)
        subcategory_2 = Category.objects.create(
            name="Gaming Laptops", parent=subcategory_1
        )

        self.assertEqual(subcategory_2.parent, subcategory_1)
        self.assertEqual(subcategory_1.parent, parent_category)


class ProductModelTestCase(TestCase):
    def setUp(self) -> None:
        # Create a Category instance
        self.category = Category.objects.create(name="Electronics")

        # Create a Supplier instance
        self.supplier = Supplier.objects.create(
            name="Tech Supplies Co.", email="supplier@example.com"
        )

        # Create a Product instance
        self.product = Product.objects.create(
            name="Smartphone",
            description="A high-end smartphone.",
            price=Decimal("999.99"),
            stock_quantity=50,
            is_active=True,
            category=self.category,
            reorder_threshold=10,
            supplier=self.supplier,
        )

    def test_product_creation(self) -> None:
        self.assertEqual(self.product.name, "Smartphone")
        self.assertEqual(self.product.description, "A high-end smartphone.")
        self.assertEqual(self.product.price, Decimal("999.99"))
        self.assertEqual(self.product.stock_quantity, 50)
        self.assertTrue(self.product.is_active)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.supplier, self.supplier)

    def test_needs_reorder(self) -> None:
        self.assertFalse(self.product.needs_reorder())
        self.product.stock_quantity = 5
        self.product.save()
        self.assertTrue(self.product.needs_reorder())

    def test_supplier_share(self) -> None:
        expected_share = float(self.product.price) * SUPPLIER_SHARE
        self.assertEqual(self.product.supplier_share(), expected_share)

    def test_product_str(self) -> None:
        self.assertEqual(str(self.product), "Smartphone")
