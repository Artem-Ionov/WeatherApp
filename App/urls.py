from django.urls import path
from .views import town_weather

urlpatterns = [
    path('', town_weather, name='town_weather')
]