from rest_framework import serializers

from commons.errors import ErrorCodes


class TotalRevenueSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)


class TotalRevenueInputSerializer(serializers.Serializer):
    start_date = serializers.DateField(
        required=False, format="%Y-%m-%d", input_formats=["%Y-%m-%d"]
    )
    end_date = serializers.DateField(
        required=False, format="%Y-%m-%d", input_formats=["%Y-%m-%d"]
    )

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                ErrorCodes.START_DATE_IS_GREATER_THAN_END_DATE
            )
        return attrs
