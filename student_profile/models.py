from django.db import models
from django.conf import settings
import json


def profile_photo_path(instance, filename):
    return f'student_profile/profiles/{instance.user_id}/photos/{filename}'


class Profile(models.Model):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'

    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(
        null=True, upload_to=profile_photo_path)
    address = models.CharField(max_length=255)
    services = models.TextField()
    preferences = models.TextField()
    birth_date = models.DateField()
    start_date = models.DateField()
    graduate_date = models.DateField(null=True)
    points = models.IntegerField(default=0)

    def get_public_link(self, request):
        return request.build_absolute_uri('/api/student-profile/profiles/' + str(self.user.id))


class Contact(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='contacts')
    type = models.CharField(max_length=255)
    link = models.URLField(max_length=255)


class Mark(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='marks')
    subject_name = models.CharField(max_length=255)
    mark = models.PositiveIntegerField()
    date = models.DateField()


class Experience(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='experiences')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    is_certified = models.BooleanField(default=False)


class Project(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE,  related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    position = models.CharField(max_length=255)
    link = models.URLField()
    is_cerified = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True)


class Feature(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,  related_name='features')
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)


class ToolManager(models.Manager):
    def get_profile_tools(self, profile):
        tools = []
        for project in profile.projects.all():
            for feature in project.features.all():
                for feature_tool in feature.feature_tools.all():
                    if feature_tool.tool not in tools:
                        tools.append(feature_tool.tool)
        return tools

    def get_project_tools(self, project):
        tools = []
        for feature in project.features.all():
            for feature_tool in feature.feature_tools.all():
                if feature_tool.tool not in tools:
                    tools.append(feature_tool.tool)
        return tools


class Tool(models.Model):
    objects = ToolManager()

    title = models.CharField(max_length=255)


class FeatureTool(models.Model):
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE,  related_name='feature_tools')
    tool = models.ForeignKey(
        Tool, on_delete=models.CASCADE,  related_name='tool_features')
