from turtle import update
from rest_framework import serializers
from .models import *
from .signals import vote


class VotedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotedItem
        fields = ['id', 'user_id', 'is_up', 'content_type', 'object_id']

    def create(self, validated_data):
        user_id = self.context['user_id']
        new_instance = VotedItem.objects.create(
            user_id=user_id, **validated_data)
        vote.send_robust(self.__class__, old_instance=None,
                         new_instance=new_instance)
        return new_instance


class UpdateVotedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotedItem
        fields = ['is_up']

    def update(self, instance, validated_data):
        old_instance = VotedItem(
            is_up=instance.is_up,
            user=instance.user,
            content_type=instance.content_type,
            object_id=instance.object_id
        )
        new_instance = super().update(instance, validated_data)
        vote.send_robust(self.__class__, old_instance=old_instance,
                         new_instance=new_instance)
        return new_instance
