# Generated by Django 4.0.4 on 2022-07-30 19:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='voteditem',
            unique_together={('user', 'content_type', 'object_id')},
        ),
    ]