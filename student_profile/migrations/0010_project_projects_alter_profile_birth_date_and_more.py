# Generated by Django 4.0.4 on 2022-08-10 22:51

from django.db import migrations, models
import student_profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('student_profile', '0009_remove_membership_is_accepted_project_photo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='projects',
            field=models.ManyToManyField(through='student_profile.Membership', to='student_profile.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='graduate_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=student_profile.models.profile_photo_path),
        ),
    ]