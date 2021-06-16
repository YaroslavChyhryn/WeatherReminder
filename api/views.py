from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from .serializers import WeatherSerializer, SubscriptionSerializer
from weather.models import Subscription, City
from django.shortcuts import get_object_or_404
import requests
from django.conf import settings
import json
import openweather_api


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    list - all of user subscriptions
    retrieve - specific subscription by id
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        subscriptions = user.subscription.all()
        return subscriptions

    def retrieve(self, request, pk, *args, **kwargs):
        subscription = get_object_or_404(Subscription, pk=pk)
        serializer = SubscriptionSerializer(subscription, context={'request': request})
        return Response(serializer.data)


class WeatherViewSet(viewsets.ViewSet):
    """
    list - Weather in cities the user is subscribed to.
    retrieve - Weather in specific city, the user does not need to be subscribed
    """
    def list(self, request):
        cities_ids = request.user.subscription.all().values_list('city___openweather_id')
        cities_ids = [city[0] for city in cities_ids]
        cities_weather_data = openweather_api.get_weather(cities_ids)

        return Response(cities_weather_data)

    def retrieve(self, request, pk,  *args, **kwargs):
        openweather_id = pk
        city_weather = openweather_api.get_weather([openweather_id])
        return Response(city_weather)
