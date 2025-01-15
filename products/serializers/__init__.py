from rest_framework import serializers

from products.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model."""

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock_quantity",
            "is_active",
            "reorder_threshold",
            "category",
            "supplier",
        ]
        read_only_fields = ["id"]


class SubcategorySerializer(serializers.ModelSerializer):
    """Recursive serializer for nested categories."""

    subcategories = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "parent", "subcategories", "products"]
        read_only_fields = ["id"]

    def get_subcategories(self, obj):
        # Recursive logic for subcategories
        queryset = obj.subcategories.all()
        serializer = SubcategorySerializer(queryset, many=True)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for creating and listing categories."""

    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "parent", "subcategories"]
        read_only_fields = ["id"]

    def get_subcategories(self, obj):
        # For flat listing of immediate subcategories
        return SubcategorySerializer(obj.subcategories.all(), many=True).data
