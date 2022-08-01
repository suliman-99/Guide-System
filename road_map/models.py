from django.db import models
from django.conf import settings


def page_background_path(instance, filename):
    return f'road_map/pages/{instance.id}/backgrounds/{filename}'


def page_icon_path(instance, filename):
    return f'road_map/pages/{instance.id}/icons/{filename}'


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
    background = models.ImageField(upload_to=page_background_path)
    icon = models.ImageField(upload_to=page_icon_path)
    view_template = models.TextField(null=True)
    importance_and_advantages = models.TextField()
    advice_and_tools = models.TextField()


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
        unique_together = [['parent', 'child'], ['parent', 'index']]


class ReferenceFeature(models.Model):
    reference = models.ForeignKey(
        Reference, on_delete=models.CASCADE, related_name='features')
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name='references')
    value = models.CharField(max_length=255)

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
