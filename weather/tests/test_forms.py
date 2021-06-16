from django.test import TestCase
from weather.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def test_city_name_max_length(self):
        form = SubscriptionForm({'city_name': 'test'*500})
        self.assertFalse(form.is_valid())

    def test_wrong_period(self):
        form = SubscriptionForm({'period': -1})
        self.assertFalse(form.is_valid())
