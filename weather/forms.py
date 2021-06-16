from django.forms import ModelForm, TextInput, Form
from .models import City, Subscription
from django import forms


class SubscriptionForm(Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  to_field_name='_openweather_id',
                                  empty_label=None,
                                  label='City')
    period = forms.ChoiceField(label='Reminding',
                               choices=Subscription.Period.choices,
                               initial=Subscription.Period.NO_REMINDING)
