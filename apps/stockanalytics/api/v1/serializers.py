# apps/stockstats/api/v1/serializers.py

from rest_framework import serializers
from apps.stockanalytics.models import StockPrice

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = ['price', 'last_updated_at']
