from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.html import format_html


def profile_photo_path(instance, filename):
    return f'student_profile/profiles/photos/{instance.user.username}_{filename}'


def project_photo_path(instance, filename):
    return f'student_profile/projects/photos/{instance.title}_{filename}'


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
        null=True, upload_to=profile_photo_path, blank=True)
    address = models.CharField(max_length=255)
    services = models.TextField()
    preferences = models.TextField()
    birth_date = models.DateField()
    start_date = models.DateField()
    graduate_date = models.DateField(null=True, blank=True)
    points = models.IntegerField(default=0)

    def get_public_link(self, request):
        return request.build_absolute_uri('/api/student-profile/profiles/' + str(self.user.id))

    def __str__(self) -> str:
        try:
            return self.user.username
        except:
            return 'No User'

    @cached_property
    def display_photo(self):
        html = '<img src="{photo}" width=100 height=100 />'
        if self.photo:
            return format_html(html, photo=self.photo.url)
        return format_html('<strong>There is no Photo for this entry.<strong>')
    display_photo.short_description = 'Display Photo'


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
    end_date = models.DateField(null=True, blank=True)
    is_certified = models.BooleanField(default=False)


class ProjectManager(models.Manager):
    def get_profile_projects(self, profile):
        projects = []
        for membership in profile.memberships.all():
            projects.append(membership.project)
        return projects


class Project(models.Model):
    objects = ProjectManager()

    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    is_certified = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    photo = models.ImageField(
        null=True, upload_to=project_photo_path)

    profiles = models.ManyToManyField(
        Profile, through='Membership', related_name='projects')

    @cached_property
    def display_photo(self):
        html = '<img src="{photo}" width=100 height=100 />'
        if self.photo:
            return format_html(html, photo=self.photo.url)
        return format_html('<strong>There is no Photo for this entry.<strong>')
    display_photo.short_description = 'Display Photo'


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
        for membership in profile.memberships.all():
            for feature in membership.project.features.all():
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


class MembershipManager(models.Manager):
    def create_or_update(self, profile, project, position, is_admin):
        try:
            membership = self.get(
                profile=profile,
                project=project
            )
            membership.position = position
            membership.is_admin = is_admin
            membership.save()
            return membership
        except:
            return self.create(
                project=project,
                profile=profile,
                position=position,
                is_admin=is_admin
            )


class Membership(models.Model):
    objects = MembershipManager()

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE,  related_name='memberships')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,  related_name='memberships')
    position = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ['profile', 'project']


class MembershipRequest(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE,  related_name='membership_requests')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,  related_name='membership_requests')
    position = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['profile', 'project']
