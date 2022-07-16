from django.contrib import admin
from .models import *

models = (VotedItem)

admin.site.register(models)
