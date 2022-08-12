from django.contrib.auth.models import AbstractUser, Group as BaseGroup
from django.db import models

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta(AbstractUser.Meta):
        pass
        # proxy = True


class Group(BaseGroup):
    class Meta:
        proxy = True
