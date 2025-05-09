from django.db import models
from django.utils import timezone
from apps.numstats.choices import NumberChoices,StatusChoices 


class Number(models.Model):
    number_id = models.CharField(max_length=10, choices=NumberChoices)
    value = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.SmallIntegerField(
        choices=StatusChoices, default=StatusChoices.CREATE
    )
