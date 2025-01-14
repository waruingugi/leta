from django.urls import path

from users.views.customers import (
    CustomerCreateView,
    CustomerListView,
    CustomerRetrieveUpdateView,
)

app_name = "customers"

urlpatterns = [
    path("create/", CustomerCreateView.as_view(), name="create"),
    path("", CustomerListView.as_view(), name="list"),
    path("<str:id>/", CustomerRetrieveUpdateView.as_view(), name="detail"),
]
