from django.urls import path
from .views import get_statistic


urlpatterns = [
    path('', get_statistic, name='statistics'),
]