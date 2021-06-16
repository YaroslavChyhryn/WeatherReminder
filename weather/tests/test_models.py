from django.test import TestCase
from weather.models import Subscription, City
from django.contrib.auth import get_user_model


class TestCityModel(TestCase):
    def test_city_openweather_id_creation(self):
        city = City(name='kyiv')
        self.assertEqual(city.openweather_id, 703448)

    def test_city_name_that_doesnt_exist(self):
        City(name='doest_exist')
        self.assertFalse(City.objects.filter(name='doest_exist').exists())


class TestSubscriptionModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        test_user = user_model(username='test_user',
                               email='test@mail.com',
                               password='test_user_password')
        test_user.save()
        city = City(name='kyiv')
        city.save()
        test_subscription = Subscription(user=test_user,
                                         city=city)
        test_subscription.save()

    def test_subscription_default_period(self):
        subscription = Subscription.objects.last()
        self.assertEqual(subscription.reminding_time_period, Subscription.Period.NO_REMINDING)
