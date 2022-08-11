from django.contrib import admin
from .models import *


class MarkInline(admin.TabularInline):
    model = Mark
    extra = 0


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0
    readonly_fields = ['id', 'name', 'type', 'description',
                       'start_date', 'end_date']


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)
    list_display = ['id', 'title', 'description',  'link', 'display_photo',
                    'is_certified', 'start_date', 'end_date']
    list_editable = ['is_certified']
    readonly_fields = ['title', 'description', 'link', 'display_photo', 'photo',
                       'start_date', 'end_date']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = (MarkInline, ExperienceInline, MembershipInline, )
    list_display = ['user_id', 'username', 'gender',
                    'birth_date', 'start_date', 'graduate_date']

    list_editable = ['gender', 'birth_date', 'start_date', 'graduate_date']

    readonly_fields = ['user', 'user_id', 'display_photo', 'photo', 'address',
                       'services', 'preferences', 'points']
    ordering = ['user_id']

    @admin.display(ordering='user__username')
    def username(self, profile):
        return profile.user.username
