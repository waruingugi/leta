from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from commons.constants import MembershipLevel
from users.models import Customer, User


class UserModelTests(TestCase):
    def setUp(self) -> None:
        self.name = "John Doe"
        self.email = "johndoe@example.com"

        self.password = uuid4().hex
        self.phone_number = "0704845040"

        self.user_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }

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

    def test_email_is_unique(self) -> None:
        """Test creating a user with a duplicate email raises a ValidationError."""
        User.objects.create_user(
            name="user1", email="email1@email.com", password=self.user_data["password"]
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                name="user2",
                email="email1@email.com",
                password=self.user_data["password"],
            )

    def test_phone_number_is_unique(self) -> None:
        """Test creating a user with a duplicate phone_number raises a ValidationError."""
        User.objects.create_user(
            name="user3",
            email="email3@email.com",
            password=self.user_data["password"],
            phone_number="+254700000003",
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                name="user4",
                email="email4@email.com",
                password=self.user_data["password"],
                phone_number="+254700000003",
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


class CustomerModelTests(TestCase):
    def setUp(self) -> None:
        self.name = "John Doe"
        self.email = "johndoe@example.com"
        self.password = uuid4().hex

        self.password = uuid4().hex
        self.user = User.objects.create_user(
            name=self.name,
            email=self.email,
            password=self.password,
        )

    def test_create_customer(self) -> None:
        """
        Test that a customer can be created and is linked to a user.
        """
        customer = Customer.objects.create(user=self.user)
        self.assertEqual(customer.user, self.user)
        self.assertEqual(customer.membership, MembershipLevel.BRONZE.value)

    def test_customer_default_membership(self) -> None:
        """
        Test that the default membership level is BRONZE.
        """
        customer = Customer.objects.create(user=self.user)
        self.assertEqual(customer.membership, MembershipLevel.BRONZE.value)

    def test_customer_membership_discount(self) -> None:
        """
        Test that the discount property returns the correct value.
        """
        customer = Customer.objects.create(
            user=self.user, membership=MembershipLevel.SILVER.value
        )
        self.assertEqual(customer.discount, MembershipLevel.SILVER.discount)

        customer.membership = MembershipLevel.GOLD.value
        self.assertEqual(customer.discount, MembershipLevel.GOLD.discount)

    def test_customer_string_representation(self) -> None:
        """
        Test the string representation of the Customer model.
        """
        customer = Customer.objects.create(user=self.user)
        self.assertEqual(str(customer), self.user.email)
