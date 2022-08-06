from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from forum.signals import *
from vote.signals import *
from forum.models import *


@receiver(vote)
def on_vote(sender, **kwargs):
    print('--------------on_vote-----------------')
    old_instance = kwargs['old_instance']
    new_instance = kwargs['new_instance']
    forum_content_type = ContentType.objects.get_for_model(Forum)
    reply_content_type = ContentType.objects.get_for_model(Reply)

    if not old_instance:
        if new_instance.content_type == forum_content_type:
            instance = Forum.objects.get(pk=new_instance.object_id)
        if new_instance.content_type == reply_content_type:
            instance = Reply.objects.get(pk=new_instance.object_id)
    elif not new_instance:
        if old_instance.content_type == forum_content_type:
            instance = Forum.objects.get(pk=old_instance.object_id)
        if old_instance.content_type == reply_content_type:
            instance = Reply.objects.get(pk=old_instance.object_id)
    else:
        if old_instance.content_type == forum_content_type and new_instance.content_type == forum_content_type:
            instance = Forum.objects.get(pk=old_instance.object_id)
        if old_instance.content_type == reply_content_type and new_instance.content_type == reply_content_type:
            instance = Reply.objects.get(pk=old_instance.object_id)

    points_diff = 0
    if old_instance:
        if old_instance.is_up:
            print('there is old instance ------- up')
            points_diff -= 1
        else:
            print('there is old instance ------- down')
            points_diff += 1
    if new_instance:
        if new_instance.is_up:
            print('there is new instance ------- up')
            points_diff += 1
        else:
            print('there is new instance ------- down')
            points_diff -= 1
    print(points_diff)
    if points_diff:
        instance.points += points_diff
        instance.save()
        vote_effect.send_robust(Forum, instance=instance,
                                points_diff=points_diff)
    print(instance)
