from django.conf import settings
from django.db import models


class Forum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_question = models.BooleanField()
    closed_reply = models.ForeignKey(
        'Reply', on_delete=models.SET_NULL, null=True, related_name='+')
    time = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    forum = models.ForeignKey(
        Forum, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
