# apps/stockstats/services.py

import requests
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now, timedelta
from apps.stockanalytics.models import StockPrice
from django.db.models import Avg
import numpy as np
import secret

class StockService:
    BASE_URL = "http://20.244.56.144/evaluation-service/stocks"
    API_TOKEN = secret.API_TOKEN

    @staticmethod
    def fetch_and_store_stock_prices(ticker: str, minutes: int):
        headers = {
            "Authorization": f"Bearer {StockService.API_TOKEN}"
        }
        try:
            url = f"{StockService.BASE_URL}/{ticker}?minutes={minutes}"
            response = requests.get(url, timeout=0.5,headers=headers)
            
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):  
                data = [data['stock']]

            for entry in data:
                price = entry["price"]
                timestamp = parse_datetime(entry["lastUpdatedAt"])
                StockPrice.objects.update_or_create(
                    ticker=ticker,
                    last_updated_at=timestamp,
                    defaults={"price": price}
                )
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data for {ticker}: {e}")

    @staticmethod
    def get_average_price(ticker: str, minutes: int):
        cutoff_time = now() - timedelta(minutes=minutes)
        recent_prices = StockPrice.objects.filter(
            ticker=ticker,
            last_updated_at__gte=cutoff_time
        ).order_by("last_updated_at")

        avg_price = recent_prices.aggregate(avg=Avg("price"))["avg"]
        return avg_price, list(recent_prices.values("price", "last_updated_at"))

    @staticmethod
    def get_price_history(ticker: str, minutes: int):
        cutoff_time = now() - timedelta(minutes=minutes)
        return StockPrice.objects.filter(
            ticker=ticker,
            last_updated_at__gte=cutoff_time
        ).order_by("last_updated_at")

    @staticmethod
    def compute_correlation(ticker1: str, ticker2: str, minutes: int):
        prices1 = StockService.get_price_history(ticker1, minutes)
        prices2 = StockService.get_price_history(ticker2, minutes)

        # Create aligned time series by timestamps
        price_dict1 = {p.last_updated_at: p.price for p in prices1}
        price_dict2 = {p.last_updated_at: p.price for p in prices2}
        common_times = sorted(set(price_dict1.keys()) & set(price_dict2.keys()))

        if len(common_times) < 2:
            return None, list(prices1), list(prices2)  # Not enough data to correlate

        x = np.array([price_dict1[t] for t in common_times])
        y = np.array([price_dict2[t] for t in common_times])

        correlation = float(np.corrcoef(x, y)[0, 1])
        return correlation, list(prices1), list(prices2)
