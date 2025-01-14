from uuid import uuid4

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from commons.tests.base import UserBaseAPITestCase
from users.models import User


class UserCreateViewTests(UserBaseAPITestCase):
    def setUp(self) -> None:
        self.url = reverse("users:create")
        self.data = {
            "phone_number": "0703245678",
            "name": "john",
            "email": "john@email.com",
            "password": uuid4().hex,
        }
        self.force_authenticate_staff_user()

    def test_staff_creates_user_successfully(self) -> None:
        """Assert endpoint creates user successfully."""
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)
        self.assertIn("phone_number", response.data)
        self.assertIn("name", response.data)

        self.assertFalse(response.data["is_verified"])
        self.assertTrue(response.data["is_active"])

        user = User.objects.get(email=self.data["email"])
        # Assert that the password is not stored as plain text
        self.assertNotEqual(user.password, self.data["password"])

    def test_email_is_required(self) -> None:
        """Assert validation error is raised if email field is missing."""
        data = self.data.copy()
        data.pop("email")  # Remove the email
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_phone_number_is_invalid(self) -> None:
        """Assert validation error is raised if phone number is invalid."""
        data = {"phone_number": "070324", "password": "password124"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_non_staff_users_can_not_create_user(self) -> None:
        """Assert users do not have permission to create users."""
        self.force_authenticate_user()
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserListViewTests(UserBaseAPITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            name="john",
            email="john@email.com",
            password=uuid4().hex,
            is_verified=True,
            is_active=True,
        )
        self.url = reverse("users:list")
        self.force_authenticate_staff_user()

    def test_staff_can_list_of_users(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], User.objects.count())

    def test_non_user_can_not_list_users(self) -> None:
        client = APIClient()
        access_token = self.create_access_token(self.user)
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserRetrieveUpdateViewTests(UserBaseAPITestCase):
    def setUp(self) -> None:
        self.user = self.create_user()
        self.force_authenticate_user()
        self.detail_url = reverse("users:detail", kwargs={"id": self.user.id})

    def test_read_only_fields_can_not_be_updated(self) -> None:
        """Assert the phone number field can not be edited."""
        data = {
            "phone_number": self.user.phone,
            "is_staff": True,
            "is_active": False,
            "is_verified": True,
        }
        response = self.client.put(self.detail_url, data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, data["phone_number"])
        self.assertFalse(response.data["is_verified"])
        self.assertFalse(response.data["is_staff"])
        self.assertTrue(response.data["is_active"])

    def test_view_retrieves_user_data(self) -> None:
        """Assert expected fields are returned in detail view."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("phone_number", response.data)
        self.assertIn("name", response.data)
        self.assertIn("is_verified", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("is_staff", response.data)

    def test_user_can_only_retrieve_their_own_data(self) -> None:
        """Assert user can only view their own data."""
        self.staff_user = self.create_staff_user()
        self.detail_url = reverse("users:detail", kwargs={"id": self.staff_user.id})
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
