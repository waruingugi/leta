from rest_framework import serializers

from products.models import Product


class BestSellingProductSerializer(serializers.ModelSerializer):
    total_sold = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ["id", "name", "total_sold"]


class BestSellingProductInputSerializer(serializers.Serializer):
    limit = serializers.IntegerField(required=False, min_value=0)
