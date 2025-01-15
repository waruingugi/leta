from django.urls import include, path

from analytics.routes import analytics

urlpatterns = [
    path("analytics/", include((analytics.urlpatterns, "analytics"))),
]
