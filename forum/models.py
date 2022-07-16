from django.db import models
from django.contrib.auth.models import User


class Forum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_question = models.BooleanField()
    is_closed = models.BooleanField(default=False)
    closed_reply = models.ForeignKey(
        'Reply', on_delete=models.SET_NULL, null=True, related_name='closed_forum')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.user} : {self.content}'


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} on {self.forum} : {self.content}'
