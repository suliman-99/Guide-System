from django.contrib import admin
from django.http import HttpRequest
from django import forms
from nonrelated_inlines.admin import NonrelatedTabularInline, NonrelatedStackedInline
from .models import *


class ContentInline(admin.StackedInline):
    model = Content
    classes = ['collapse']
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3, 'cols': 50})},
        models.CharField: {'widget': forms.Textarea(
            attrs={'rows': 1, 'cols': 23})}
    }


class FeedbackInline(admin.TabularInline):
    model = Feedback
    classes = ['collapse']
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3, 'cols': 50})},
    }


class DependencyInline(admin.TabularInline):
    model = Dependency
    classes = ['collapse']
    extra = 0
    fk_name = 'parent'
    autocomplete_fields = ['child']


class ReferenceInline(admin.TabularInline):
    model = Reference
    classes = ['collapse']
    extra = 0
    fk_name = 'parent'
    autocomplete_fields = ['child']
    show_change_link = True


class FeatureInline(admin.TabularInline):
    model = Feature
    classes = ['collapse']
    extra = 0


class ReferenceFeatureInline(NonrelatedTabularInline):
    model = ReferenceFeature
    classes = ['collapse']
    extra = 0
    fields = ['reference_child', 'feature_name', 'value']
    readonly_fields = ['reference_child', 'feature_name']
    ordering = ['reference__child__id', 'feature__name']

    def reference_child(self, reference_feature):
        return reference_feature.reference.child

    def feature_name(self, reference_feature):
        return reference_feature.feature.name

    def get_form_queryset(self, obj):
        return ReferenceFeature.objects \
            .select_related('feature__page') \
            .select_related('reference__parent') \
            .select_related('reference__child') \
            .filter(feature__page=obj) \
            .order_by('reference__child__id', 'feature__name')

    def save_new_instance(self, parent, instance):
        pass


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):

    def get_inlines(self, request: HttpRequest, obj):
        if obj:
            if obj.type == Page.TYPE_OR:
                return (FeedbackInline, DependencyInline, ReferenceInline, FeatureInline, ReferenceFeatureInline)
            elif obj.type == Page.TYPE_AND:
                return (FeedbackInline, DependencyInline, ReferenceInline)
            else:
                return (ContentInline, FeedbackInline, DependencyInline)
        return []

    def get_fieldsets(self, request: HttpRequest, obj):
        if obj:
            return (
                (None, {
                    'fields': (
                        "title",
                        "type",
                        ("icon", "display_clickable_icon_photo"),
                        ("background", "display_clickable_background_photo"),
                        "importance_and_advantages",
                        "advice_and_tools",
                    )
                }),
            )
        else:
            return (
                (None, {
                    'fields': (
                        "title",
                        "type",
                        "icon",
                        "background",
                        "importance_and_advantages",
                        "advice_and_tools",
                    )
                }),
            )

    def get_readonly_fields(self, request: HttpRequest, obj):
        if obj:
            return ['display_clickable_background_photo', 'display_clickable_icon_photo']
        else:
            return []

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3, 'cols': 50})},
    }

    def save_formset(self, request, form, formset, change) -> None:
        added_instances = formset.save(commit=True)
        deleted_instances = formset.deleted_objects
        formset.save()
        if added_instances:
            if isinstance(added_instances[0], Feature):
                references = Reference.objects.filter(
                    parent_id=added_instances[0].page)
                for feature in added_instances:
                    feature.save()
                    for reference in references:
                        ReferenceFeature.objects.get_or_create(
                            reference=reference, feature=feature, value='')
            if isinstance(added_instances[0], Reference):
                features = Feature.objects.filter(
                    page_id=added_instances[0].parent)
                for reference in added_instances:
                    reference.save()
                    for feature in features:
                        ReferenceFeature.objects.get_or_create(
                            reference=reference, feature=feature, value='')
                Reference.ensure_page_references_order_unique_and_from_zero(
                    added_instances[0].parent.id)
        return

    # ----------------------------------------------------------------------

    list_display = ['id', 'title', 'type',
                    'display_clickable_background_photo', 'display_clickable_icon_photo']

    list_display_links = ['id', 'title']

    ordering = ['id']

    list_filter = ['type']

    search_fields = ['title']
