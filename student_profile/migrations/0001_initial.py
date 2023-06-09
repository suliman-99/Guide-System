# Generated by Django 4.1 on 2023-03-22 20:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import student_profile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=255)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('photo', models.ImageField(blank=True, max_length=500, null=True, upload_to=student_profile.models.profile_photo_path)),
                ('address', models.CharField(max_length=255)),
                ('services', models.TextField()),
                ('preferences', models.TextField()),
                ('birth_date', models.DateField()),
                ('start_date', models.DateField()),
                ('graduate_date', models.DateField(blank=True, null=True)),
                ('points', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('link', models.URLField()),
                ('is_certified', models.BooleanField(default=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, max_length=500, null=True, upload_to=student_profile.models.project_photo_path)),
                ('profiles', models.ManyToManyField(related_name='projects', through='student_profile.Membership', to='student_profile.profile')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='student_profile.profile'),
        ),
        migrations.AddField(
            model_name='membership',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='student_profile.project'),
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=255)),
                ('mark', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='student_profile.profile')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureTool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_tools', to='student_profile.feature')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tool_features', to='student_profile.tool')),
            ],
        ),
        migrations.AddField(
            model_name='feature',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='student_profile.project'),
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_certified', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='student_profile.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='student_profile.profile')),
            ],
        ),
        migrations.CreateModel(
            name='MembershipRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=255)),
                ('is_admin', models.BooleanField(default=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_requests', to='student_profile.profile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_requests', to='student_profile.project')),
            ],
            options={
                'unique_together': {('profile', 'project')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('profile', 'project')},
        ),
    ]
