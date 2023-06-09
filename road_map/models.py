from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.html import format_html


def page_background_path(instance, filename):
    return f'road_map/pages/backgrounds/{instance.title}_{filename}'


def page_icon_path(instance, filename):
    return f'road_map/pages/icons/{instance.title}_{filename}'


class Page(models.Model):

    TYPE_LEAF = 'L'
    TYPE_OR = 'O'
    TYPE_AND = 'A'

    TYPE_CHOICES = [
        (TYPE_LEAF, 'Leaf'),
        (TYPE_OR, 'Or'),
        (TYPE_AND, 'And')
    ]

    title = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    background = models.ImageField(upload_to=page_background_path, max_length=500)
    icon = models.ImageField(upload_to=page_icon_path, max_length=500)
    importance_and_advantages = models.TextField()
    advice_and_tools = models.TextField()
    reference_next_index = models.IntegerField(default=0)

    @cached_property
    def display_background(self):
        html = '<img src="{background}" width=100 height=100 />'
        if self.background:
            return format_html(html, background=self.background.url)
        return format_html('<strong>There is no background for this entry.<strong>')
    display_background.short_description = 'Background'

    @cached_property
    def display_icon(self):
        html = '<img src="{icon}" width=100 height=100 />'
        if self.icon:
            return format_html(html, icon=self.icon.url)
        return format_html('<strong>There is no icon for this entry.<strong>')
    display_icon.short_description = 'Icon'

    @cached_property
    def display_clickable_background_photo(self):
        html = '<a href="{link}"><img src="{photo}" width=100 height=100 /></a>'
        return format_html(html, link=self.background.url, photo=self.background.url)
    display_clickable_background_photo.short_description = 'Background'

    @cached_property
    def display_clickable_icon_photo(self):
        html = '<a href="{link}"><img src="{photo}" width=100 height=100 /></a>'
        return format_html(html, link=self.icon.url, photo=self.icon.url)
    display_clickable_icon_photo.short_description = 'Icon'

    def __str__(self) -> str:
        return self.title


class Feature(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ['page', 'name']


class Reference(models.Model):
    parent = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='reference_children')
    child = models.ForeignKey(
        Page, on_delete=models.PROTECT, related_name='reference_parents')
    index = models.PositiveIntegerField()

    class Meta:
        unique_together = [['parent', 'child']]

    def __str__(self) -> str:
        return f'{self.parent} - {self.child}'

    @classmethod
    def ensure_page_references_order_unique_and_from_zero(self, page_id):
        count = 0
        for reference in self.objects.filter(parent_id=page_id).order_by('index'):
            if reference.index != count:
                reference.index = count
                reference.save()
            count += 1


class ReferenceFeature(models.Model):
    reference = models.ForeignKey(
        Reference, on_delete=models.CASCADE, related_name='features')
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name='references')
    value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ['reference', 'feature']


class Dependency(models.Model):
    parent = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='dependency_children')
    child = models.ForeignKey(
        Page, on_delete=models.PROTECT, related_name='dependency_parents')

    class Meta:
        unique_together = ['parent', 'child']


class Content(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField(max_length=255)


class Feedback(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='feedbacks')
    content = models.TextField()


class FinishedPage(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='finished_users')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['page', 'user']
