from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from weather.models import Subscription, City


class CitySerializer(serializers.ModelSerializer):
    """
    Serialize City model
    """
    class Meta:
        model = City
        fields = ['name', 'openweather_id']
        extra_kwargs = {'name': {'validators': []}}


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize Subscription model, crate and update subscription
    """
    city = CitySerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    url = serializers.HyperlinkedIdentityField(view_name="api:subscriptions-detail")

    class Meta:
        model = Subscription
        fields = ['id', 'url', 'city', 'hook_url', 'reminding_time_period', 'user']

    def create(self, validated_data):
        city, created = City.objects.get_or_create(name=validated_data['city']['name'].lower())
        city.openweather_id
        subscription, created = Subscription.objects.get_or_create(city=city,
                                                                   user=validated_data['user'])
        if validated_data['reminding_time_period']:
            subscription.reminding_time_period = validated_data['reminding_time_period']
        return subscription

    def update(self, instance, validated_data):
        instance.hook_url = validated_data.get('hook_url', instance.hook_url)
        instance.reminding_time_period = validated_data.get('reminding_time_period', instance.reminding_time_period)
        instance.save()
        return instance


class WeatherSerializer(serializers.Serializer):
    """
    Serialize Weather
    """
    city_name = serializers.CharField(max_length=255)
    temperature = serializers.IntegerField()
    description = serializers.CharField(max_length=255)
