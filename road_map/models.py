from msilib.schema import TypeLib
from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):

    TYPE_LEAF = 'L'
    TYPE_OR = 'O'
    TYPE_AND = 'A'

    TYPE_CHOICES = [
        (TYPE_LEAF, 'Leaf'),
        (TYPE_OR, 'Or'),
        (TYPE_AND, 'And')
    ]

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    background = models.ImageField()
    icon = models.ImageField()
    view_template = models.TextField(null=True)
    importance_and_advantages = models.TextField()
    advice_and_tools = models.TextField()

    students = models.ManyToManyField(User, through='FinishedPage')
    dependencies = models.ManyToManyField(
        'Page', related_name='related_dependencies')
    references = models.ManyToManyField(
        'Page', related_name='related_references', through='PageReference')

    def __str__(self):
        return self.title


class PageReferencesFeature(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f' {self.page} - {self.name}'

    class Meta:
        db_table = 'road_map_page_references_feature'


class PageReference(models.Model):
    parent_page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name='reference_children_set')
    referenced_page = models.ForeignKey(
        Page, on_delete=models.PROTECT, related_name='reference_parent_set')
    index = models.PositiveIntegerField()
    features = models.ManyToManyField(
        PageReferencesFeature, related_name='page_references', through='Feature')

    def __str__(self):
        return f' {self.index} - {self.parent_page} -> {self.referenced_page}'

    class Meta:
        db_table = 'road_map_page_reference'


class Feature(models.Model):
    page_reference = models.ForeignKey(
        PageReference, on_delete=models.CASCADE, related_name='features_set')
    page_references_feature = models.ForeignKey(
        PageReferencesFeature, on_delete=models.CASCADE, related_name='references_set')
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.page_reference.parent_page} - {self.page_references_feature.name} : {self.value}'


class Content(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField(max_length=255)

    def __str__(self):
        return f'{self.page} -> {self.title} : {self.content} \n {self.link}'


class Feedback(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content


class FinishedPage(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student} : {self.page}'
