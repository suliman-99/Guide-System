from django.db import models
from django.db.models.aggregates import Count
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class VotedItemManager(models.Manager):

    def get_object_vote_data(self, content_type, object_id, user_id):
        try:
            content_type = int(content_type)
        except:
            content_type = ContentType.objects.get(model=content_type).id
        up = self.filter(content_type=content_type,
                         object_id=object_id, is_up=True).aggregate(Count('pk'))['pk__count']
        down = self.filter(content_type=content_type,
                           object_id=object_id, is_up=False).aggregate(Count('pk'))['pk__count']
        votedItems = self.filter(content_type=content_type, object_id=object_id,
                                 user_id=user_id).only('id', 'is_up')
        if votedItems:
            votedItem = votedItems[0]
        else:
            votedItem = None
        data = {}
        data['vote_value'] = up - down
        if not votedItem:
            data['is_my_vote_exist'] = False
            data['my_vote'] = "None"
        else:
            data['is_my_vote_exist'] = True
            data['my_vote'] = {
                'id': votedItem.id,
                'is_up': votedItem.is_up
            }

        return data


class VotedItem(models.Model):
    objects = VotedItemManager()

    is_up = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
