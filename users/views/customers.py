from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView

from commons.pagination import StandardPageNumberPagination
from commons.permissions import IsStaffPermission
from users.models import Customer
from users.serializers.customers import (
    CustomerCreateSerializer,
    CustomerListSerializer,
    CustomerRetrieveUpdateSerializer,
)


class CustomerCreateView(CreateAPIView):
    """Create a customer."""

    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer
    permission_classes = [IsStaffPermission]


class CustomerListView(ListAPIView):
    """List customers."""

    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    permission_classes = [IsStaffPermission]
    pagination_class = StandardPageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = ["user__email", "user__phone_number", "membership"]
    filterset_fields = ["membership"]
    ordering_fields = ["created_at"]


class CustomerRetrieveUpdateView(RetrieveUpdateAPIView):
    """Retrieve or update a customer."""

    lookup_field = "id"
    queryset = Customer.objects.all()
    permission_classes = [IsStaffPermission]
    serializer_class = CustomerRetrieveUpdateSerializer
