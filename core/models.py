from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import UUIDField

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(unique=True)
