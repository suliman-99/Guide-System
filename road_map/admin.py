from django.contrib import admin
from .models import *


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', 'display_background', 'display_icon', 'view_template',
                    'importance_and_advantages', 'advice_and_tools']


@admin.register(Dependency)
class DependencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(ReferenceFeature)
class ReferenceFeatureAdmin(admin.ModelAdmin):
    pass


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    pass


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    pass


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass
