from django.test import TestCase, Client
from weather.models import City, Subscription
from django.test.utils import override_settings
from allauth.account import app_settings as account_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

@override_settings(
    SOCIALACCOUNT_AUTO_SIGNUP=True,
    ACCOUNT_SIGNUP_FORM_CLASS=None,
    ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.NONE  # noqa
)
class WeatherViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_users = 2
        cities = ['kyiv', 'london', 'paris', 'tokyo']

        for user_num in range(number_of_users):
            user = User.objects.create(username=f'user_{user_num}',
                                       email=f'user_{user_num}@mail.com',
                                       password='password')
            user.save()

            for _ in range(2):
                city = City(name=cities.pop())
                city.save()
                subscription = Subscription(user=user,
                                            city=city)
                subscription.save()

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_city_list(self):
        resp = self.client.get(reverse('weather:index'))
        weather_data = resp.context['weather_data']
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('Tokyo', weather_data[0]['city_name'])
        self.assertTemplateUsed(resp, 'weather/subscription_list.html')

    def test_city_create(self):
        resp = self.client.post(reverse('weather:city_create'), {'city_name': 'Dubai',
                                                                 'period': Subscription.Period.NO_REMINDING})

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(self.user.subscription.filter(city__name='dubai').exists())

    def test_city_update(self):
        subscription = self.user.subscription.all()[0]
        city = subscription.city
        resp = self.client.post(reverse('weather:city_update', kwargs={'pk': city.id}),
                                {'hook_url': subscription.hook_url,
                                 'reminding_time_period': Subscription.Period.EVERY_3_HOUR})
        self.assertEqual(resp.status_code, 302)
        subscription = self.user.subscription.all()[0]
        self.assertEqual(subscription.reminding_time_period, Subscription.Period.EVERY_3_HOUR)

    def test_city_delete(self):
        subscription = self.user.subscription.all()[0]
        city = subscription.city
        resp = self.client.post(reverse('weather:city_delete', kwargs={'pk': city.id}))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(self.user.subscription.filter(city__name=city.name).exists())

    def test_test_mixin(self):
        user_2 = User.objects.get(pk=2)
        subscription = user_2.subscription.all()[0]
        city = subscription.city
        resp = self.client.post(reverse('weather:city_delete', kwargs={'pk': city.id}))
        self.assertEqual(resp.status_code, 403)
