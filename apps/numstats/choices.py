from django.db import models


class StatusChoices(models.IntegerChoices):
    DELETE = 0
    CREATE = 1
    UPDATE = 2


class NumberChoices(models.TextChoices):
    PRIME = 'p', 'Prime'
    EVEN = 'e', 'Even'
    FIBONACCI = 'f', 'Fibonacci'
    RANDOM = 'r', 'Random'
