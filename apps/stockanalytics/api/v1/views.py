# apps/stockstats/api/v1/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.stockanalytics.api.v1.services import StockService
from .serializers import StockPriceSerializer

class StockAverageView(APIView):
    def get(self, request, ticker):
        minutes = int(request.GET.get("minutes", 5))
        aggregation = request.GET.get("aggregation", "average")

        StockService.fetch_and_store_stock_prices(ticker, minutes)
        avg_price, price_history = StockService.get_average_price(ticker, minutes)

        serializer = StockPriceSerializer(price_history, many=True)

        return Response({
            "averageStockPrice": avg_price,
            "priceHistory": serializer.data
        })


class StockCorrelationView(APIView):
    def get(self, request):
        minutes = int(request.GET.get("minutes", 5))
        tickers = request.GET.getlist("ticker")

        if len(tickers) != 2:
            return Response(
                {"error": "Exactly 2 tickers are required for correlation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        ticker1, ticker2 = tickers
        StockService.fetch_and_store_stock_prices(ticker1, minutes)
        StockService.fetch_and_store_stock_prices(ticker2, minutes)

        correlation, prices1, prices2 = StockService.compute_correlation(ticker1, ticker2, minutes)

        serializer1 = StockPriceSerializer(prices1, many=True)
        serializer2 = StockPriceSerializer(prices2, many=True)

        return Response({
            "correlation": correlation,
            "stocks": {
                ticker1: {
                    "averagePrice": StockService.get_average_price(ticker1, minutes)[0],
                    "priceHistory": serializer1.data
                },
                ticker2: {
                    "averagePrice": StockService.get_average_price(ticker2, minutes)[0],
                    "priceHistory": serializer2.data
                }
            }
        })
