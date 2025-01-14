from uuid import uuid4

from django.core.exceptions import ValidationError
from django.test import TestCase

from users.models import User


class UserModelTests(TestCase):
    def setUp(self) -> None:
        self.name = "John Doe"
        self.email = "johndoe@example.com"
        self.password = uuid4().hex
        self.user_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
        self.phone_number = "0704845040"

    def test_create_user_success(self) -> None:
        user = User.objects.create_user(
            name=self.user_data["name"],
            email=self.user_data["email"],
            password=self.user_data["password"],
            phone_number=self.phone_number,
        )
        self.assertEqual(user.name, self.name)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(user.phone_number, self.phone_number)
        self.assertFalse(user.is_staff)

    def test_create_user_missing_email(self) -> None:
        """Test creating a user without an email raises a ValidationError."""
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                name=self.user_data["name"],
                email="",
                password=self.user_data["password"],
            )

    def test_create_user_missing_name(self) -> None:
        """Test creating a user without a name raises a ValidationError."""
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                name="",
                email=self.user_data["email"],
                password=self.user_data["password"],
            )

    def test_create_superuser_success(self) -> None:
        """Test that a superuser can be created successfully."""
        superuser = User.objects.create_superuser(
            name=self.user_data["name"],
            email=self.user_data["email"],
            password=self.user_data["password"],
            phone_number=self.phone_number,
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_superuser_without_staff_or_superuser_flag(self) -> None:
        """Test that creating a superuser without proper flags raises an error."""
        with self.assertRaises(ValidationError):
            User.objects.create_superuser(
                name=self.user_data["name"],
                email=self.user_data["email"],
                password=self.user_data["password"],
                phone_number=self.phone_number,
                is_staff=False,
            )
        with self.assertRaises(ValidationError):
            User.objects.create_superuser(
                name=self.user_data["name"],
                email=self.user_data["email"],
                password=self.user_data["password"],
                phone_number=self.phone_number,
                is_superuser=False,
            )

    def test_user_string_representation(self) -> None:
        """Test the string representation of a user."""
        user = User.objects.create_user(
            name=self.user_data["name"],
            email=self.user_data["email"],
            password=self.user_data["password"],
        )
        self.assertEqual(str(user), self.user_data["email"])
