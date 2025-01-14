from django.test import TestCase

from products.models import Category


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
