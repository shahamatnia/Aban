from rest_framework import serializers
from src.models import Cryptocurrency, PurchaseOrder


class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = ['name', 'price']

