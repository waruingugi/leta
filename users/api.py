from django.urls import include, path

from users.routes import auth

urlpatterns = [path("auth/", include((auth.urlpatterns, "auth")))]
