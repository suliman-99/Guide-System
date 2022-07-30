from rest_framework import serializers
from .models import *


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'user_id', 'content', 'time']


class CreateReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['content']

    def create(self, validated_data):
        user_id = self.context['user_id']
        forum_id = self.context['forum_id']
        return Reply.objects.create(user_id=user_id, forum_id=forum_id, **validated_data)


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['id', 'user_id', 'title', 'content', 'is_question', 'time', 'is_closed',
                  'closed_reply', 'replies']

    is_closed = serializers.SerializerMethodField()
    closed_reply = ReplySerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    def get_is_closed(self, forum):
        return forum.closed_reply is not None


class CreateForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['title', 'content', 'is_question']

    def create(self, validated_data):
        user_id = self.context['user_id']
        return Forum.objects.create(user_id=user_id, **validated_data)
