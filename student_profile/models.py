from django.db import models
from django.conf import settings


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
    points = models.PositiveBigIntegerField(default=0)
    photo = models.ImageField(null=True, upload_to='photos')
    address = models.CharField(max_length=255)
    services = models.TextField()
    preferences = models.TextField()
    birth_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    def get_public_link(self, request):
        return request.build_absolute_uri('/api/student-profile/profiles/' + str(self.user.id))


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    is_cerified = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    members = models.ManyToManyField(
        Profile, through='Membership', related_name='projects')


class Membership(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='memberships')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='memberships')
    position = models.CharField(max_length=255)

    class Meta:
        unique_together = ('profile', 'project')


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
