from django.urls import path
from apps.numstats.api.v1.views import NumberView

urlpatterns = [
    path('numbers/<str:numberid>', NumberView.as_view(), name='number_view'),
]
