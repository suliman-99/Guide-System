from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group as BaseGroup
from rest_framework.authtoken.models import TokenProxy
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.http import HttpRequest
from .models import User, Group
from student_profile.models import Profile


admin.site.unregister(TokenProxy)
admin.site.unregister(BaseGroup)
admin.site.register(Group, BaseGroupAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile
    min_num = 0
    max_num = 1
    fields = ['gender', 'birth_date', 'start_date', 'graduate_date']


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    def get_queryset(self, request: HttpRequest):
        if not request.user.is_superuser:
            return super().get_queryset(request).filter(is_superuser=False, is_staff=False)
        return super().get_queryset(request)

    def get_fieldsets(self, request: HttpRequest, obj):
        if not obj:
            return (
                (None, {
                    'classes': ('wide',),
                    'fields': ("username", "email", "first_name", "last_name", "password1", "password2")}
                 ),
            )
        if not request.user.is_superuser:
            return (
                (None, {
                 'fields': ("username", "password", "email", "first_name", "last_name")}),
                (_('Permissions'), {
                    'fields': ('is_active',),
                }),
            )
        return super().get_fieldsets(request, obj)
