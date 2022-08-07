from rest_framework import serializers
from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'number_of_uses']


class AppliedTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedTag
        fields = ['id', 'tag', 'tag_name', 'content_type', 'object_id']

    tag = TagSerializer(read_only=True)
    tag_name = serializers.CharField(write_only=True)

    def create(self, validated_data):
        (tag, _) = Tag.objects.get_or_create(
            name=validated_data.pop('tag_name'))
        return AppliedTag.objects.create(tag=tag, **validated_data)


class SuggestedTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedTag
        fields = ['id', 'tag', 'tag_name',
                  'content_type', 'object_id', 'is_add']

    tag = TagSerializer(read_only=True)
    tag_name = serializers.CharField(write_only=True)

    def create(self, validated_data):
        (tag, _) = Tag.objects.get_or_create(
            name=validated_data.pop('tag_name'))
        return SuggestedTag.objects.create(tag=tag, **validated_data)
