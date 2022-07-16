from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    TYPE_GOOD = 'G'
    TYPE_BAD = 'B'
    TYPE_CHOICES = [
        (TYPE_GOOD, 'Good'),
        (TYPE_BAD, 'Bad')
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    number_of_uses = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    contnet_object = GenericForeignKey()

    def __str__(self):
        return self.tag


class SuggestedTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    contnet_object = GenericForeignKey()

    # descripe if this tag suggested to add or to delete
    is_add = models.BooleanField()

    def __str__(self):
        return self.tag
