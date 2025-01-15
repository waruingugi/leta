from django.urls import path

from analytics.views.products import BestSellingProductsView
from analytics.views.revenue import TotalRevenueView

app_name = "analytics"

urlpatterns = [
    path("revenue/", TotalRevenueView.as_view(), name="total-revenue"),
    path(
        "best-selling-products/",
        BestSellingProductsView.as_view(),
        name="best-selling-products",
    ),
]
