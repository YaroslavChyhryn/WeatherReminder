from .django import env
from celery.schedules import crontab


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

OPENWEATHER_API_KEY = env('OPENWEATHER_API_KEY')

ENVIRONMENT_NAME = env('ENVIRONMENT_NAME')
ENVIRONMENT_COLOR = env('ENVIRONMENT_COLOR')

# django-allauth
AUTH_USER_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
# ACCOUNT_ADAPTER = 'accounts.adapter.MyAccountAdapter'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False

# crispy_forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# celery
CELERY_BROKER_URL = env('REDIS_URL')
CELERY_CELERY_RESULT_BACKEND = env('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Kiev'

# CELERY_BEAT_SCHEDULE = {
#     "weather_notification_by_email_every_1_hour": {
#         "task": "weather_email_notification",
#         "schedule": crontab(minute='0', hour='*/1'),
#         "args": (1,),
#     },
#     "weather_notification_by_email_every_3_hour": {
#         "task": "weather_email_notification",
#         "schedule": crontab(minute='0', hour='*/3'),
#         "args": (3,),
#     },
#     "weather_notification_by_email_every_6_hour": {
#         "task": "weather_email_notification",
#         "schedule": crontab(minute='0', hour='*/6'),
#         "args": (6,),
#     },
#     "weather_notification_by_email_every_12_hour": {
#         "task": "weather_email_notification",
#         "schedule": crontab(minute='0', hour='*/12'),
#         "args": (12,),
#     },
#     "weather_notification_by_email_every_24_hour": {
#         "task": "weather_email_notification",
#         "schedule": crontab(minute='0', hour='*/24'),
#         "args": (24,),
#     },
# }
