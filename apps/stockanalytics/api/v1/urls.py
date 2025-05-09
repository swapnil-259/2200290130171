# apps/stockstats/api/v1/urls.py

from django.urls import path
from apps.stockanalytics.api.v1.views import StockAverageView, StockCorrelationView

urlpatterns = [
    path("stocks/<str:ticker>", StockAverageView.as_view(), name="stock-average"),
    path("stockcorrelation", StockCorrelationView.as_view(), name="stock-correlation"),
]
