from uuid import uuid4

from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserBaseAPITestCase(APITestCase):
    phone_number = "+254712345678"
    password = uuid4().hex
    name = "testuser"
    email = "testuser@email.com"
    staff_name = "admin"
    staff_phone_number = "0701234567"
    staff_email = "admin@email.com"
    staff_password = uuid4().hex

    def create_user(self) -> User:
        self.user = User.objects.create_user(
            name=self.name,
            email=self.email,
            password=self.password,
            phone_number=self.phone_number,
        )
        return self.user

    def create_staff_user(self) -> User:
        self.staff_user = User.objects.create_user(
            phone_number=self.staff_phone_number,
            name=self.staff_name,
            email=self.staff_email,
            password=self.staff_password,
            is_staff=True,
            is_verified=True,
        )
        return self.staff_user

    def force_authenticate_user(self) -> None:
        self.client = APIClient()
        if not hasattr(self, "user"):
            self.user = self.create_user()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def force_authenticate_staff_user(self) -> None:
        if not hasattr(self, "staff_user"):
            self.create_staff_user()

        self.client = APIClient()
        self.client.force_authenticate(user=self.staff_user)

    def create_access_token(self, user) -> str:
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
