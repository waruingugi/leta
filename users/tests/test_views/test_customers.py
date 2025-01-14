from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from commons.constants import MembershipLevel
from commons.tests.base import UserBaseAPITestCase
from users.models import Customer


class CustomerCreateViewTests(UserBaseAPITestCase):
    def setUp(self) -> None:
        self.url = reverse("customers:create")
        self.user = self.create_user()
        self.data = {
            "user": self.user.id,
            "membership": MembershipLevel.BRONZE.value,
        }
        self.force_authenticate_staff_user()

    def test_staff_creates_customer_successfully(self) -> None:
        """Assert endpoint creates customer successfully."""
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertIn("membership", response.data)

        customer = Customer.objects.get(user=self.user)
        self.assertEqual(customer.membership, self.data["membership"])

    def test_membership_defaults_to_bronze(self) -> None:
        """Assert membership defaults to 'BRONZE' if not provided."""
        data = {"user": self.user.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["membership"], MembershipLevel.BRONZE.value)

    def test_non_staff_users_cannot_create_customer(self) -> None:
        """Assert only staff users can create customers."""
        self.force_authenticate_user()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_is_required(self) -> None:
        """Assert validation error is raised if user field is missing."""
        data = {"membership": MembershipLevel.SILVER.value}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user", response.data)


class CustomerListViewTests(UserBaseAPITestCase):
    def setUp(self) -> None:
        self.url = reverse("customers:list")
        self.user = self.create_user()
        self.customer = Customer.objects.create(
            user=self.user, membership=MembershipLevel.GOLD.value
        )
        self.force_authenticate_staff_user()

    def test_staff_can_list_customers(self) -> None:
        """Assert staff can list customers."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Customer.objects.count())
        self.assertIn("email", response.data["results"][0])
        self.assertIn("phone_number", response.data["results"][0])

    def test_non_staff_users_cannot_list_customers(self) -> None:
        """Assert non-staff users cannot list customers."""
        client = APIClient()
        access_token = self.create_access_token(self.user)
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CustomerRetrieveUpdateViewTests(UserBaseAPITestCase):
    def setUp(self) -> None:
        self.user = self.create_user()
        self.customer = Customer.objects.create(
            user=self.user, membership=MembershipLevel.SILVER.value
        )
        self.detail_url = reverse("customers:detail", kwargs={"id": self.customer.id})
        self.force_authenticate_staff_user()

    def test_staff_can_update_membership(self) -> None:
        """Assert staff can update the membership of a customer."""
        data = {"membership": MembershipLevel.GOLD.value}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.membership, MembershipLevel.GOLD.value)

    def test_read_only_fields_cannot_be_updated(self) -> None:
        """Assert user field cannot be updated."""
        data = {"name": "New Name", "membership": MembershipLevel.GOLD.value}
        response = self.client.put(self.detail_url, data)

        self.assertEqual(response.data["name"], self.user.name)
        self.assertEqual(response.data["membership"], MembershipLevel.GOLD.value)

    def test_view_retrieves_customer_data(self) -> None:
        """Assert expected fields are returned in detail view."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("membership", response.data)
        self.assertIn("id", response.data)

    def test_non_staff_users_cannot_access_detail_view(self) -> None:
        """Assert non-staff users cannot retrieve or update customers."""
        client = APIClient()
        access_token = self.create_access_token(self.user)
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
