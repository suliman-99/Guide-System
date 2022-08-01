from django.contrib import admin
from .models import *

models = (Page, Reference, Feedback, FinishedPage, Content, ReferenceFeature)

admin.site.register(models)
