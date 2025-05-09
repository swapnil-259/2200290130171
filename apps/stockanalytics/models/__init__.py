from django.db import models

class StockPrice(models.Model):
    ticker = models.CharField(max_length=10, db_index=True)
    price = models.FloatField()
    last_updated_at = models.DateTimeField()