from django.urls import include, path

from products.routes import categories

urlpatterns = [
    path("categories/", include((categories.urlpatterns, "categories"))),
]
