from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.serializers.products import (
    BestSellingProductInputSerializer,
    BestSellingProductSerializer,
)
from commons.constants import BEST_SELLING_PRODUCTS_LIMIT
from products.models import Product


class BestSellingProductsView(APIView):
    """Endpoint to retrieve the top N best-selling products."""

    def get(self, request):
        # Retrieve the limit from serializers
        input_serializer = BestSellingProductInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)
        limit = input_serializer.validated_data.get(
            "limit", BEST_SELLING_PRODUCTS_LIMIT
        )

        # Annotate products with total quantity sold
        best_selling_products = (
            Product.objects.annotate(total_sold=Sum("order_items__quantity"))
            .filter(total_sold__isnull=False)  # Exclude products with no sales
            .order_by("-total_sold")[:limit]
        )

        # Serialize the response
        serializer = BestSellingProductSerializer(best_selling_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
