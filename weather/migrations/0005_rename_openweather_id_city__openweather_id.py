# Generated by Django 3.2.3 on 2021-05-31 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_alter_city_openweather_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='openweather_id',
            new_name='_openweather_id',
        ),
    ]