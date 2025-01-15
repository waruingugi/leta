from django.urls import path

from products.views.categories import (
    CategoryCreateView,
    CategoryListView,
    CategoryRetrieveUpdateView,
    NestedCategoryProductsView,
)

app_name = "categories"

urlpatterns = [
    path("create/", CategoryCreateView.as_view(), name="create"),
    path("", CategoryListView.as_view(), name="list"),
    path("<str:id>/", CategoryRetrieveUpdateView.as_view(), name="detail"),
    path(
        "<str:id>/nested-products/",
        NestedCategoryProductsView.as_view(),
        name="nested-products",
    ),
]
