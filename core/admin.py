from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import User
from student_profile.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    min_num = 0
    max_num = 1
    fields = ['gender', 'birth_date', 'start_date', 'graduate_date']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_select_related = ('profile', )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )


try:
    from rest_framework.authtoken.models import TokenProxy as DRFToken
except ImportError:
    from rest_framework.authtoken.models import Token as DRFToken

admin.site.unregister(DRFToken)
