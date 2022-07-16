from django.contrib import admin
from .models import *

models = (Forum, Reply)

admin.site.register(models)