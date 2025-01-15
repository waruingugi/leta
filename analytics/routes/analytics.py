from django.urls import path

from analytics.views.revenue import TotalRevenueView

app_name = "analytics"

urlpatterns = [
    path("revenue/", TotalRevenueView.as_view(), name="total-revenue"),
]
