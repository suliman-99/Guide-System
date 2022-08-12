from django.contrib import admin
from django.forms import Textarea
from django.http import HttpRequest
from .models import *


class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 0

    def get_fields(self, request: HttpRequest, obj):
        return ('id', 'name', 'type', 'description', 'start_date', 'end_date', 'is_certified')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 80, 'rows': 5})},
    }


class MarkInline(admin.TabularInline):
    model = Mark
    extra = 0


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    def get_inlines(self, request: HttpRequest, obj):
        return (MembershipInline,
                )

    def get_list_display(self, request: HttpRequest):
        return ['id', 'title', 'description',  'link', 'display_photo',
                'is_certified', 'start_date', 'end_date']

    def get_list_display_links(self, request: HttpRequest, list_display):
        return ['user_id', 'username']

    def get_readonly_fields(self, request: HttpRequest, obj):
        return ['title', 'description', 'link', 'display_photo', 'photo',
                'start_date', 'end_date']

    # def get_ordering(self, request: HttpRequest):
    #     return ['user_id']

    # list_editable = ['is_certified']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    # list_editable = ['gender', 'birth_date', 'start_date', 'graduate_date']

    def get_inlines(self, request: HttpRequest, obj):
        return (MembershipInline, MarkInline, ExperienceInline)

    def get_list_display(self, request: HttpRequest):
        return ['user_id', 'username', 'gender',
                'birth_date', 'start_date', 'graduate_date']

    def get_list_display_links(self, request: HttpRequest, list_display):
        return ['user_id', 'username']

    def get_ordering(self, request: HttpRequest):
        return ['user_id']

    def get_fields(self, request: HttpRequest, obj):
        return (('user_id', 'username', 'points'), 'photo', 'address', 'services',
                'preferences', ('birth_date', 'gender'), ('start_date', 'graduate_date'))

    def get_readonly_fields(self, request: HttpRequest, obj):
        return ['user_id', 'username', 'display_photo', 'photo', 'address',
                'services', 'preferences', 'points']

    # def get_list_filter(self, request: HttpRequest):
    #     return super().get_list_filter(request)

    # def get_search_fields(self, request: HttpRequest):
    #     return super().get_search_fields(request)

    # def get_fieldsets(self, request: HttpRequest, obj):
    #     return super().get_fieldsets(request, obj)

    # def get_exclude(self, request: HttpRequest, obj):
    #     return super().get_exclude(request, obj)

    @ admin.display(ordering='user__username')
    def username(self, profile):
        return profile.user.username
