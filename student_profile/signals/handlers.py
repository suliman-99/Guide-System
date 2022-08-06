from django.dispatch import receiver
from forum.signals import *
from student_profile.models import Profile


@receiver(forum_close)
def on_forum_closed(sender, **kwargs):
    old_reply = kwargs['old_reply']
    new_reply = kwargs['new_reply']
    if old_reply:
        old_profile = Profile.objects.get(pk=old_reply.user.id)
        old_profile.points -= 1
        old_profile.save()
    if new_reply:
        new_profile = Profile.objects.get(pk=new_reply.user.id)
        new_profile.points += 1
        new_profile.save()


@receiver(vote_effect)
def on_forum_vote(sender, **kwargs):
    instance = kwargs['instance']
    points_diff = kwargs['points_diff']
    profile = Profile.objects.get(pk=instance.user.id)
    if points_diff:
        profile.points += points_diff
        profile.save()
