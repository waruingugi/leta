from rest_framework import serializers

from users.models import Customer


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["user", "membership"]


class CustomerBaseDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone_number", "membership"]
        extra_kwargs = {"membership": {"required": False}}
        read_only_fields = ["id", "name", "email", "phone_number"]


class CustomerListSerializer(CustomerBaseDetailSerializer):
    class Meta(CustomerBaseDetailSerializer.Meta):
        pass


class CustomerRetrieveUpdateSerializer(CustomerBaseDetailSerializer):
    class Meta(CustomerBaseDetailSerializer.Meta):
        pass
