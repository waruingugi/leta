from django.test import TestCase

from products.models import Category, Product


class CategoryModelTests(TestCase):
    def test_category_creation(self):
        """Test the creation of a category without parent."""
        category = Category.objects.create(name="Electronics")
        self.assertEqual(category.name, "Electronics")
        self.assertIsNone(category.parent)

    def test_category_creation_with_parent(self):
        """Test the creation of a category with a parent."""
        parent_category = Category.objects.create(name="Electronics")
        child_category = Category.objects.create(name="Laptops", parent=parent_category)

        self.assertEqual(child_category.name, "Laptops")
        self.assertEqual(child_category.parent, parent_category)

    def test_parent_child_relationship(self):
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

    def test_category_str_method(self):
        """Test the string representation of the category."""
        category = Category.objects.create(name="Electronics")
        self.assertEqual(str(category), "Electronics")

    def test_top_level_category(self):
        """Test top-level category (without parent)."""
        category = Category.objects.create(name="Furniture")
        self.assertIsNone(category.parent)

    def test_subcategory_of_subcategory(self):
        """Test the subcategory of a subcategory."""
        parent_category = Category.objects.create(name="Electronics")
        subcategory_1 = Category.objects.create(name="Laptops", parent=parent_category)
        subcategory_2 = Category.objects.create(
            name="Gaming Laptops", parent=subcategory_1
        )

        self.assertEqual(subcategory_2.parent, subcategory_1)
        self.assertEqual(subcategory_1.parent, parent_category)


class ProductModelTests(TestCase):
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            description="A high-end smartphone with great features.",
            price=699.99,
            stock_quantity=50,
            is_active=True,
            category=self.category,
            reorder_threshold=10,
        )

    def test_product_creation(self):
        """Test that a Product instance is created correctly."""
        product = Product.objects.get(name="Smartphone")
        self.assertEqual(
            product.description, "A high-end smartphone with great features."
        )
        self.assertEqual(str(product.price), str(699.99))
        self.assertEqual(product.stock_quantity, 50)
        self.assertTrue(product.is_active)
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.reorder_threshold, 10)

    def test_needs_reorder_true(self):
        """Test that the needs_reorder method returns True when stock is below threshold."""
        self.product.stock_quantity = 5
        self.product.save()
        self.assertTrue(self.product.needs_reorder())

    def test_needs_reorder_false(self):
        """Test that the needs_reorder method returns False when stock is above threshold."""
        self.product.stock_quantity = 20
        self.product.save()
        self.assertFalse(self.product.needs_reorder())

    def test_category_relationship(self):
        """Test the relationship between Product and Category."""
        self.assertEqual(self.product.category.name, "Electronics")

    def test_str_method(self):
        """Test the __str__ method of the Product model."""
        self.assertEqual(str(self.product), "Smartphone")
