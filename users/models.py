# Create your models here.
from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from commons.constants import MembershipLevel
from commons.models import Base


class UserManager(BaseUserManager):
    def create_user(
        self,
        *,
        name: str,
        email: str,
        password: str,
        phone_number: PhoneNumberField | None = None,
        **extra_fields: Any,
    ) -> "User":
        if not email:
            raise ValidationError(_("User must have an email."))

        if not name:
            raise ValidationError(_("User must have a name."))

        email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number, name=name.title(), email=email, **extra_fields
        )
        user.set_password(password)  # type: ignore
        user.save(using=self.db)

        return user  # type: ignore

    def create_superuser(
        self,
        *,
        name: str,
        email: str,
        password: str,
        phone_number: PhoneNumberField | None = None,
        **extra_fields: Any,
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValidationError(_("Superuser must have is_staff=True."))
        if not extra_fields.get("is_superuser"):
            raise ValidationError(_("Superuser must have is_superuser=True."))

        return self.create_user(
            phone_number=phone_number,
            name=name,
            email=email,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin, Base):
    """The default user model"""

    name = models.CharField(blank=False, null=False, max_length=20)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = ["name"]  # type: ignore

    def __str__(self) -> str:
        return self.email or self.name

    @property
    def phone(self) -> str:
        return str(self.phone_number)

    class Meta:
        ordering = ("-created_at",)


class Customer(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    membership = models.CharField(
        max_length=10,
        choices=[(level.value, level.value) for level in MembershipLevel],
        default=MembershipLevel.BRONZE.value,
    )

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.user.email

    @property
    def discount(self) -> float:
        return MembershipLevel(self.membership).discount
