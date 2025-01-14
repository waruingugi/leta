from rest_framework import serializers

from commons.errors import ErrorCodes
from users.models import User


class PhoneNumberIsAvailableValidator:
    def __call__(self, phone) -> None:
        if User.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError(ErrorCodes.PHONE_NUMBER_EXISTS.value)
