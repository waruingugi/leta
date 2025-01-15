from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from commons.errors import ErrorCodes
from products.models import Category
from products.serializers.categories import (
    CategoryCreateSerializer,
    CategoryListSerializer,
    CategoryRetrieveUpdateSerializer,
    SubcategorySerializer,
)


class CategoryCreateView(CreateAPIView):
    """Create a new category."""

    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


class CategoryListView(ListAPIView):
    """List all categories, including their immediate subcategories."""

    queryset = Category.objects.filter(parent__isnull=True)  # Only top-level categories
    serializer_class = CategoryListSerializer


class CategoryRetrieveUpdateView(RetrieveUpdateAPIView):
    """Retrieve or update a specific category."""

    queryset = Category.objects.all()
    serializer_class = CategoryRetrieveUpdateSerializer
    lookup_field = "id"


class NestedCategoryProductsView(APIView):
    """Fetch all products in a category, including nested subcategories."""

    serializer_class = SubcategorySerializer

    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response(
                {"detail": ErrorCodes.CATEGORY_DOES_NOT_EXIST.value}, status=404
            )

        # Serialize the category with nested products and subcategories
        serializer = SubcategorySerializer(category)
        return Response(serializer.data)
