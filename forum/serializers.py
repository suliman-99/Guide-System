from rest_framework import serializers
from tag.serializers import AppliedTagSerializer

from vote.models import VotedItem
from .models import *


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'user_id', 'content',
                  'time', 'points', 'is_mine', 'vote_data']

    is_mine = serializers.SerializerMethodField()
    vote_data = serializers.SerializerMethodField()

    def get_is_mine(self, forum):
        return bool(self.context['user_id'] and forum.user.id == self.context['user_id'])

    def get_vote_data(self, reply):
        return VotedItem.objects.get_object_vote_data('reply', reply.id, self.context['user_id'])


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
        fields = ['id', 'user_id', 'title', 'content', 'is_question', 'time', 'points', 'is_closed',
                  'closed_reply', 'is_mine', 'vote_data', 'tags', 'suggested_tags']

    closed_reply = ReplySerializer(read_only=True)
    is_closed = serializers.SerializerMethodField()
    is_mine = serializers.SerializerMethodField()
    vote_data = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    suggested_tags = serializers.SerializerMethodField()

    def get_is_closed(self, forum):
        return forum.closed_reply is not None

    def get_is_mine(self, forum):
        return bool(self.context['user_id'] and self.context['user_id'] == forum.user.id)

    def get_vote_data(self, forum):
        return VotedItem.objects.get_object_vote_data('forum', forum.id, self.context['user_id'])

    def get_tags(self, forum):
        return AppliedTagSerializer(AppliedTag.objects.get_object_tags(
            'forum',
            forum.id,
        ),
            many=True,
        ).data

    def get_suggested_tags(self, forum):
        if self.context['user_id'] and self.context['user_id'] == forum.user.id:
            return AppliedTagSerializer(SuggestedTag.objects.get_object_tags(
                'forum',
                forum.id,
            ),
                many=True,
            ).data
        return {}


class CreateForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['title', 'content', 'is_question']

    def create(self, validated_data):
        user_id = self.context['user_id']
        return Forum.objects.create(user_id=user_id, **validated_data)
