from rest_framework import serializers

from products.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model."""

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "name",
            "is_active",
        ]


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


class CategoryBaseSerializer(serializers.ModelSerializer):
    """Base Serializer for creating and listing categories."""

    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "parent", "subcategories"]
        read_only_fields = ["id", "parent", "subcategories"]

    def get_subcategories(self, obj):
        # For flat listing of immediate subcategories
        return SubcategorySerializer(obj.subcategories.all(), many=True).data


class CategoryCreateSerializer(CategoryBaseSerializer):
    class Meta(CategoryBaseSerializer.Meta):
        pass


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryRetrieveUpdateSerializer(CategoryBaseSerializer):
    class Meta(CategoryBaseSerializer.Meta):
        pass
