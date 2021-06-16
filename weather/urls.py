from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.CityList.as_view(), name='index'),
    path('profile/', views.user_setting, name='user_settings'),
    path('city/create/', views.CityCreate.as_view(), name='city_create'),
    path('city/update/<int:pk>/', views.CityUpdate.as_view(), name='city_update'),
    path('city/delete/<int:pk>/', views.CityDelete.as_view(), name='city_delete'),
]
