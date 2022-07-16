from django.contrib import admin
from .models import *

models = (Page, PageReference, Feedback, FinishedPage, Content, Feature)

admin.site.register(models)