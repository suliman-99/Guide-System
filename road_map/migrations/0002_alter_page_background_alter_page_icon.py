# Generated by Django 4.0.4 on 2022-07-31 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('road_map', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='background',
            field=models.ImageField(upload_to='road_map/pages/backgrounds'),
        ),
        migrations.AlterField(
            model_name='page',
            name='icon',
            field=models.ImageField(upload_to='road_map/pages/icons'),
        ),
    ]