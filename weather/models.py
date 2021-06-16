from django.db import models
from django.conf import settings
import requests
from django_extensions.db.fields import AutoSlugField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import Http404
import json
from django.contrib import messages
from openweather_api import get_openweather_id
from django.db.models.signals import post_save


class City(models.Model):
    """
    City model
    """
    name = models.CharField(max_length=25, unique=True)
    slug = AutoSlugField(populate_from='name')
    _openweather_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "город"
        verbose_name_plural = 'города'

    @property
    def openweather_id(self):
        if self._openweather_id is None:
            openweather_id = get_openweather_id(self.name)

            if openweather_id is None:
                self.delete()
                raise Http404

            self._openweather_id = openweather_id
            self.save()

        return self._openweather_id


class Subscription(models.Model):
    """
    Subscription model
    """
    class Period(models.IntegerChoices):
        NO_REMINDING = (0, 'No reminding')
        EVERY_1_HOUR = (3600, 'Every 1 hour')
        EVERY_3_HOUR = (10800, 'Every 3 hour')
        EVERY_6_HOUR = (21600, 'Every 6 hour')
        EVERY_12_HOUR = (43200, 'Every 12 hour')
        EVERY_24_HOUR = (86400, 'Every 24 hour')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city')
    hook_url = models.CharField(max_length=255, blank=True)
    reminding_time_period = models.IntegerField(choices=Period.choices,
                                                default=Period.NO_REMINDING)

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = 'подписки'

    def _str_(self):
        return self.user.username + self.city.name


@receiver(post_save, sender=Subscription)
def create_test(sender, instance=None, created=False, **kwargs):
    """
    This signal create celery task after subscription is created
    """
    from .tasks import send_email_from_celery

    if created:
        send_email_from_celery.delay(instance.id)
