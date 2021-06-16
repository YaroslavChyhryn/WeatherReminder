from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "api"

router = DefaultRouter()
router.register(r'weather', views.WeatherViewSet, basename='weather')
router.register(r'cities', views.SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    path('', include(router.urls)),
]
