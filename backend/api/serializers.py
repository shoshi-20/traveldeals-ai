from rest_framework import serializers
from .models import Merchant, Deal


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = [
            "id",
            "title",
            "description",
            "destination",
            "price",
            "is_embedded",
            "created_at",
        ]
        read_only_fields = ["id", "is_embedded", "created_at"]


class MerchantConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ["id", "name", "brand_color", "logo_url"]
