from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedManager(models.Manager):

    def get_object_tags(self, content_type, object_id):
        try:
            content_type = int(content_type)
        except:
            content_type = ContentType.objects.get(model=content_type).id
        return self.filter(content_type=content_type, object_id=object_id)


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    number_of_uses = models.PositiveIntegerField(default=0)


class AppliedTag(models.Model):
    objects = TaggedManager()

    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    contnet_object = GenericForeignKey()

    class Meta:
        unique_together = ['tag', 'content_type', 'object_id']


class SuggestedTag(models.Model):
    objects = TaggedManager()

    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    contnet_object = GenericForeignKey()

    # descripe if this tag suggested to add or to delete
    is_add = models.BooleanField()

    class Meta:
        unique_together = ['tag', 'content_type', 'object_id']
