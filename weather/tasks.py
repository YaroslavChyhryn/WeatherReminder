from celery import shared_task, task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
import json
from .models import Subscription
import openweather_api
from django.shortcuts import get_object_or_404


@shared_task()
def send_email_from_celery(subscription_id):
    subscription = get_object_or_404(Subscription, pk=subscription_id)

    if subscription.reminding_time_period == 0:
        return

    weather = openweather_api.get_weather([subscription.city.openweather_id])

    message = json.dumps(weather, indent=4)
    mail_subject = f'Weather in {subscription.city.name} every {subscription.reminding_time_period/60/60} hour'
    to_email = subscription.user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

    print(f'Notification for {subscription.user.username} with weather in {subscription.city.name}'
          f' every {subscription.reminding_time_period/60/60} hour')
    send_email_from_celery.apply_async(args=[subscription.id], countdown=subscription.reminding_time_period)
