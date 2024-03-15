from rest_framework import serializers
from src.models import Cryptocurrency, PurchaseOrder


class PurchaseOrderSerializer(serializers.ModelSerializer):
    cryptocurrency_name = serializers.CharField(write_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'cryptocurrency_name', 'amount', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

    def create(self, validated_data):
        cryptocurrency_name = validated_data.pop('cryptocurrency_name')
        cryptocurrency = Cryptocurrency.objects.get(name=cryptocurrency_name)
        validated_data['cryptocurrency'] = cryptocurrency
        return super().create(validated_data)
