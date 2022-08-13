from django import forms
from django.contrib import admin
from django.forms import Textarea
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import *
from django.utils.translation import gettext_lazy as _


class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 0
    classes = ['collapse']
    fieldsets = (
                (None, {
                 'fields': (
                     ("name", "type"),
                     "description",
                     ("start_date", "end_date"),
                     "is_certified"
                 )
                 }),
    )

    def get_fields(self, request: HttpRequest, obj):
        return ('id', 'name', 'type', 'description', 'start_date', 'end_date', 'is_certified')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 50})},
        models.CharField: {'widget': Textarea(attrs={'rows': 1, 'cols': 23})}
    }


class MarkInline(admin.TabularInline):
    model = Mark
    extra = 0
    classes = ['collapse']


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0
    classes = ['collapse']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    def get_inlines(self, request: HttpRequest, obj):
        return (MembershipInline,)

    def get_list_display(self, request: HttpRequest):
        return ['id', 'title', 'description',  'link',  'display_photo',
                'is_certified', 'start_date', 'end_date']

    def get_list_display_links(self, request: HttpRequest, list_display):
        return ['user_id', 'username']

    def get_readonly_fields(self, request: HttpRequest, obj):
        return ['title', 'description', 'link', 'display_photo', 'photo',
                'start_date', 'end_date']

    # def get_ordering(self, request: HttpRequest):
    #     return ['user_id']

    # list_editable = ['is_certified']


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

    @ admin.display(ordering='user__username')
    def username(self, profile):
        return profile.user.username

    # list_editable = ['gender', 'birth_date', 'start_date', 'graduate_date']

    def get_list_display(self, request: HttpRequest):
        return ['user_id', 'username', 'gender',
                'birth_date', 'start_date', 'graduate_date']

    def get_list_display_links(self, request: HttpRequest, list_display):
        return ['user_id', 'username']

    def get_ordering(self, request: HttpRequest):
        return ['user_id']

    # def get_list_filter(self, request: HttpRequest):
    #     return super().get_list_filter(request)

    # def get_search_fields(self, request: HttpRequest):
    #     return super().get_search_fields(request)
