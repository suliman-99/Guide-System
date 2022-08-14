from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group as BaseGroup
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.http import HttpRequest
from .models import User, Group
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

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('groups'):
            form.cleaned_data['groups'] = form.cleaned_data.pop(
                'groups').filter(name='student')
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change) -> None:
        added_instances = formset.save(commit=False)
        deleted_instances = formset.deleted_objects
        user = User.objects.get(username=form.cleaned_data['username'])
        group, _ = Group.objects.get_or_create(name='student')
        if len(added_instances) == 1 and isinstance(added_instances[0], Profile):
            user.groups.add(group)
        elif len(deleted_instances) == 1 and isinstance(deleted_instances[0], Profile):
            user.groups.remove(group)
        else:
            try:
                if user.profile:
                    user.groups.add(group)
            except:
                user.groups.remove(group)
        return super().save_formset(request, form, formset, change)


admin.site.unregister(BaseGroup)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    def get_queryset(self, request: HttpRequest):
        if not request.user.is_superuser:
            return super().get_queryset(request).filter(name='student')
        return super().get_queryset(request)
