from django.contrib import admin
from .models import *

models = (Profile, Contact, Mark, Experience, Project)

admin.site.register(models)
