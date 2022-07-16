from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'

    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    ]

    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    points = models.PositiveBigIntegerField()
    photo = models.ImageField(null=True)
    address = models.CharField(max_length=255)
    services = models.TextField()
    preferences = models.TextField()
    birth_date = models.DateField()
    is_graduated = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    link = models.URLField(max_length=255)

    def __str__(self):
        return f'{self.type} : {self.link}'


class Mark(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=255)
    mark = models.PositiveIntegerField()
    data = models.DateField()

    def __str__(self):
        return f'{self.subject_name} : {self.mark}'


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    is_certified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type} : {self.name}'


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    is_cerified = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    members = models.ManyToManyField(
        Profile, through='Membership', verbose_name='members')

    def __str__(self):
        return self.title


class Membership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.project} - {self.position} - {self.profile}'
