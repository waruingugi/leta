from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from commons.serializers import UserPhoneNumberField
from users.models import User
from users.validators import PhoneNumberIsAvailableValidator


class UserCreateSerializer(serializers.ModelSerializer):
    phone_number = UserPhoneNumberField(
        required=False, validators=[PhoneNumberIsAvailableValidator()]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],  # Use Django's built-in validators
    )

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "password",
            "is_active",
            "is_verified",
            "is_staff",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_active": {"read_only": True},
            "is_verified": {"read_only": True},
        }

    def create(self, validated_data):
        # Extract password and hash it
        password = validated_data.pop("password", None)
        user = self.Meta.model(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "email",
            "phone_number",
            "is_active",
            "is_verified",
            "is_staff",
        ]
        extra_kwargs = {"name": {"required": False}}
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "email",
            "phone_number",
            "is_verified",
            "is_active",
            "is_staff",
        ]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
