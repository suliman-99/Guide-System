from rest_framework import serializers
from .models import *


class VotedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotedItem
        fields = ['id', 'user_id', 'is_up', 'content_type', 'object_id']

    def create(self, validated_data):
        user_id = self.context['user_id']
        return VotedItem.objects.create(user_id=user_id, **validated_data)


class UpdateVotedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotedItem
        fields = ['is_up']
