import requests
import json
from django.conf import settings


URL_ID = 'http://api.openweathermap.org/data/2.5/weather?id={city_id}&units=metric&appid={api_key}'
URL_GROUP = 'http://api.openweathermap.org/data/2.5/group?id={cities_id}&units=metric&appid={api_key}'
URL_CITY_NAME = 'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}'


def get_weather(cities_ids=[]):
    cities_id = [str(city_id) for city_id in cities_ids]
    cities_id = ','.join(cities_id)

    cities_weather_data = {}
    
    if len(cities_id) == 0:
        return cities_weather_data

    try:
        cities_weather = requests.get(URL_GROUP.format(cities_id=cities_id, api_key=settings.OPENWEATHER_API_KEY)).json()

        for city_weather in cities_weather['list']:
            cities_weather_data[city_weather['id']] = {
                'id': city_weather['id'],
                'city_name': city_weather['name'],
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon'],
            }
    except json.JSONDecodeError as e:
        cities_weather_data = {}

    return cities_weather_data


def get_openweather_id(city_name):
    try:
        city_weather = requests.get(URL_CITY_NAME.format(city_name=city_name,
                                                         api_key=settings.OPENWEATHER_API_KEY)).json()
    except json.JSONDecodeError as e:
        return None

    if city_weather['cod'] != 200:
        return None

    return city_weather['id']
