from datetime import datetime

from django.db.models import Sum
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.serializers.analytics import (
    TotalRevenueInputSerializer,
    TotalRevenueSerializer,
)
from commons.constants import OrderStatus
from orders.models import Order


class TotalRevenueView(APIView):
    """Endpoint to calculate total revenue within a given date range."""

    serializer_class = TotalRevenueSerializer

    def get(self, request) -> Response:
        # Validate and parse input using the serializer
        input_serializer = TotalRevenueInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data

        # Extract validated dates
        start_date = validated_data.get("start_date")
        end_date = validated_data.get("end_date")

        # Convert date to datetime and make timezone-aware
        if start_date:
            start_date = make_aware(datetime.combine(start_date, datetime.min.time()))
        if end_date:
            end_date = make_aware(datetime.combine(end_date, datetime.max.time()))

        # Filter orders by date range and status
        orders = Order.objects.filter(status=OrderStatus.COMPLETED.value)
        if start_date:
            orders = orders.filter(created_at__gte=start_date)
        if end_date:
            orders = orders.filter(created_at__lte=end_date)

        # Calculate total revenue
        total_revenue = orders.aggregate(total=Sum("total_price"))["total"] or 0

        # Return response
        return Response({"total_revenue": total_revenue}, status=status.HTTP_200_OK)
