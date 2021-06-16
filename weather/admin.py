from django.contrib import admin
from .models import City, Subscription


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Subscription)
class SubsriptionAdmin(admin.ModelAdmin):
    list_display = ('city', 'user')
