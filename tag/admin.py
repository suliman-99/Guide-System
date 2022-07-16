from django.contrib import admin
from .models import *

models = (Tag, SuggestedTag, TaggedItem)

admin.site.register(models)
