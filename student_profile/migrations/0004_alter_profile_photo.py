# Generated by Django 4.0.4 on 2022-07-31 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_profile', '0003_project_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(null=True, upload_to='student_profile/profiles/photos'),
        ),
    ]