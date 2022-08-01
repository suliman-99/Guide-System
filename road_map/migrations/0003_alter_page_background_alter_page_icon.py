# Generated by Django 4.0.4 on 2022-08-01 01:30

from django.db import migrations, models
import road_map.models


class Migration(migrations.Migration):

    dependencies = [
        ('road_map', '0002_alter_page_background_alter_page_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='background',
            field=models.ImageField(upload_to=road_map.models.page_background_path),
        ),
        migrations.AlterField(
            model_name='page',
            name='icon',
            field=models.ImageField(upload_to=road_map.models.page_icon_path),
        ),
    ]