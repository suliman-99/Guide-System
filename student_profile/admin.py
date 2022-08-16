
from django.contrib import admin
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .forms import *


class MembershipInline(admin.TabularInline):
    model = Membership
    classes = ['collapse']
    extra = 0


class MarkInline(admin.TabularInline):
    model = Mark
    classes = ['collapse']
    extra = 0


class ExperienceInline(admin.StackedInline):
    model = Experience
    classes = ['collapse']
    extra = 0

    def get_fieldsets(self, request: HttpRequest, obj):
        if request.user.is_superuser:
            return (
                (None, {
                    'fields': (
                        "name",
                        "type",
                        "description",
                        "start_date",
                        "end_date",
                        "is_certified"
                    )
                }),
            )
        else:
            return (
                (None, {
                    'fields': (
                        ("name", "type", "description"),
                        ("start_date", "end_date"),
                        ("is_certified"),
                    )
                }),
            )

    def get_readonly_fields(self, request: HttpRequest, obj):
        if request.user.is_superuser:
            return []
        else:
            return ['name', 'type', 'description', 'start_date', 'end_date']

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3, 'cols': 50})},
        models.CharField: {'widget': forms.Textarea(
            attrs={'rows': 1, 'cols': 23})}
    }


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    def get_form(self, request, obj, change, **kwargs):
        if obj:
            if request.user.is_superuser:
                return SuperuserChangeProfileForm
            return ChangeProfileForm
        return AddProfileForm

    def get_inlines(self, request: HttpRequest, obj):
        if obj:
            return (MembershipInline, MarkInline, ExperienceInline)
        return []

    def save_form(self, request, form, change):
        data = form.cleaned_data
        if change:
            user = form.instance.user
            user.username = data.pop('username', user.username)
            user.email = data.pop('email', user.email)
            user.first_name = data.pop('first_name', user.first_name)
            user.last_name = data.pop('last_name', user.last_name)
            user.is_active = data.pop('is_active', user.is_active)
            user.save()
        else:
            if data['password1'] == data.pop('password2'):
                user = get_user_model().objects.create(
                    username=data.pop('username'),
                    email=data.pop('email'),
                    first_name=data.pop('first_name'),
                    last_name=data.pop('last_name'),
                    is_active=True,
                )
                user.set_password(data.pop('password1'))
                user.save()
                group, _ = Group.objects.get_or_create(name='students')
                user.groups.add(group)
                form.instance.user = user
                form.instance.save()
        return super().save_form(request, form, change)

    def get_fieldsets(self, request: HttpRequest, obj):
        if obj:
            if request.user.is_superuser:
                return (
                    (None, {
                        'fields': (
                            "clickable_photo",
                            "photo",
                            ("username", "email"),
                            ("first_name", "last_name"),
                            ("birth_date", "gender"),
                            ("start_date", "graduate_date"),
                            "is_active"
                        )
                    }),
                )
            return (
                (None, {
                 'fields': (
                     "clickable_photo",
                     ("username", "email"),
                     ("first_name", "last_name"),
                     ("birth_date", "gender"),
                     ("start_date", "graduate_date"),
                     "is_active"
                 )
                 }),
            )
        return (
            (None, {
                'fields': (
                    ("username", "email"),
                    ("password1", "password2"),
                    ("first_name", "last_name"),
                    ("birth_date", "gender"),
                    ("start_date", "graduate_date")
                )
            }),
        )

    # ----------------------------------------------------------------------

    @ admin.display(ordering='user__username')
    def username(self, profile):
        return profile.user.username

    @ admin.display(ordering='user__email')
    def email(self, profile):
        return profile.user.email

    @ admin.display(ordering='user__first_name')
    def first_name(self, profile):
        return profile.user.first_name

    @ admin.display(ordering='user__last_name')
    def last_name(self, profile):
        return profile.user.last_name

    list_display = ['user_id', 'username', 'display_clickable_photo',
                    'first_name', 'last_name', 'gender']

    list_display_links = ['user_id', 'username']

    ordering = ['user_id']

    list_filter = ['gender', 'start_date', 'graduate_date']

    search_fields = ['user__username', 'user__email',
                     'user__first_name', 'user__last_name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    inlines = (MembershipInline,)

    list_display = ['id', 'title', 'clickable_link',  'display_clickable_photo',
                    'is_certified']

    list_display_links = ['id', 'title']

    list_editable = ['is_certified']

    ordering = ['id']

    list_filter = ['is_certified', 'start_date', 'end_date']

    search_fields = ['title', 'description']

    # ----------------------------------------------------------------------

    def get_fieldsets(self, request: HttpRequest, obj):
        if request.user.is_superuser:
            if obj:
                return (
                    (None, {
                        'fields': (
                            "title",
                            "description",
                            "link",
                            "display_clickable_photo",
                            "photo",
                            "start_date",
                            "end_date",
                            "is_certified"
                        )
                    }),
                )
            else:
                return (
                    (None, {
                        'fields': (
                            "title",
                            "description",
                            "link",
                            "photo",
                            "start_date",
                            "end_date",
                            "is_certified"
                        )
                    }),
                )
        else:
            return (
                (None, {
                    'fields': (
                        "title",
                        "description",
                        "clickable_link",
                        "display_clickable_photo",
                        "start_date",
                        "end_date",
                        "is_certified"
                    )
                }),
            )

    def get_readonly_fields(self, request: HttpRequest, obj):
        if request.user.is_superuser:
            return ['clickable_link', 'display_clickable_photo']
        else:
            return ['title', 'description', 'clickable_link', 'display_clickable_photo', 'start_date', 'end_date']
