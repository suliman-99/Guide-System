from django import forms
from django.contrib import admin
from django.forms import Textarea
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import *
from django.utils.translation import gettext_lazy as _


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
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 50})},
        models.CharField: {'widget': Textarea(attrs={'rows': 1, 'cols': 23})}
    }


class AddProfileForm(forms.ModelForm):

    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'gender', 'birth_date', 'start_date', 'graduate_date')


class ChangeProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active',
                  'gender', 'birth_date', 'start_date', 'graduate_date')

    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    is_active = forms.BooleanField()

    def get_initial_for_field(self, field, field_name):
        profile = self.instance
        if field_name == 'username':
            return profile.user.username
        elif field_name == 'email':
            return profile.user.email
        elif field_name == 'first_name':
            return profile.user.first_name
        elif field_name == 'last_name':
            return profile.user.last_name
        elif field_name == 'is_active':
            return profile.user.is_active
        return super().get_initial_for_field(field, field_name)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    def get_form(self, request, obj, **kwargs):
        if obj:
            return ChangeProfileForm
        return AddProfileForm

    def get_inlines(self, request: HttpRequest, obj):
        if obj:
            return (MembershipInline, MarkInline, ExperienceInline)
        return []

    def save_form(self, request, form, change):
        data = form.cleaned_data
        if change:
            is_active = data.pop('is_active')
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
                group, _ = Group.objects.get_or_create(name='student')
                user.groups.add(group)
                form.instance.user = user
                form.instance.save()
        return super().save_form(request, form, change)

    def get_fieldsets(self, request: HttpRequest, obj):
        if obj:
            return (
                (None, {
                 'fields': (
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

    list_display = ['user_id', 'username', 'email',
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
            return (
                (None, {
                    'fields': (
                        "title",
                        "description",
                        "link",
                        "clickable_link",
                        "photo",
                        "display_clickable_photo",
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
            return ['title', 'description', 'start_date', 'end_date', 'clickable_link', 'display_clickable_photo']
