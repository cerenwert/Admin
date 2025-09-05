from rest_framework import serializers
from .models import ModelPerson, Offer

class ModelPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPerson
        fields = ["id", "full_name"]

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ["id", "company", "model", "start_date", "end_date", "price", "status", "created_at"]
        read_only_fields = ["created_at", "status"]

    def validate(self, attrs):
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        if start and end and end < start:
            raise serializers.ValidationError("end_date start_date'ten önce olamaz.")
        price = attrs.get("price")
        if price is not None and price <= 0:
            raise serializers.ValidationError("price 0'dan büyük olmalıdır.")
        return attrs
