from django.shortcuts import render
import requests
from .models import City, Subscription
from .forms import SubscriptionForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, View
from django.views.generic.list import ListView
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from rest_framework.authtoken.models import Token
import openweather_api


class TestMixin(UserPassesTestMixin):
    """
    test for that subscription belongs to the user
    """
    def test_func(self):
        subscription = get_object_or_404(Subscription, pk=self.kwargs['pk'])
        return self.request.user.id == subscription.user.id


class CityList(LoginRequiredMixin, ListView):
    model = Subscription
    url = 'http://api.openweathermap.org/data/2.5/weather?id={city_id}&units=metric&appid={api_key}'

    def get_context_data(self, **kwargs):
        subscriptions = self.request.user.subscription.all().values_list('city___openweather_id', 'id')

        subscriptions = dict(subscriptions)
        cities_ids = subscriptions.keys()

        weather_data = openweather_api.get_weather(cities_ids)
        weather_data = list(weather_data.values())

        for city in weather_data:
            city['subs_id'] = subscriptions[city['id']]

        return {'weather_data': weather_data,
                'SubscriptionForm': SubscriptionForm}


class CityCreate(LoginRequiredMixin, FormView):
    form_class = SubscriptionForm
    template_name = 'weather/subscription_form.html'
    success_url = '/'

    def form_valid(self, form):
        city = form.cleaned_data['city']
        subscription, created = Subscription.objects.get_or_create(city=city,
                                                                   user=self.request.user)
        subscription.reminding_time_period = form.cleaned_data['period']

        if created:
            subscription.reminding_time_period = form.cleaned_data['period']
            messages.info(self.request, f'Создана подписка на {city.name}')
            subscription.save()
        else:
            messages.info(self.request, f'Вы уже подписаны на {city.name}')

        return super(CityCreate, self).form_valid(form)


class CityUpdate(LoginRequiredMixin, TestMixin, UpdateView):
    model = Subscription
    fields = ['hook_url', 'reminding_time_period']
    success_url = '/'


class CityDelete(LoginRequiredMixin, TestMixin, DeleteView):
    model = Subscription
    success_url = '/'


@login_required()
def user_setting(request):
    token = get_object_or_404(Token, user=request.user)
    return render(request, 'weather/user_setting.html', {'token': token})
