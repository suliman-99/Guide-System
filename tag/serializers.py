from rest_framework import serializers
from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'number_of_uses']


class AppliedTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedTag
        fields = ['id', 'tag_id', 'tag_name', 'tag_number_of_uses',
                  'content_type', 'object_id']

    tag_id = serializers.IntegerField(source='tag.id', read_only=True)
    tag_name = serializers.CharField(max_length=255, source='tag.name')
    tag_number_of_uses = serializers.IntegerField(
        source='tag.number_of_uses', read_only=True)

    def create(self, validated_data):
        (tag, _) = Tag.objects.get_or_create(
            name=validated_data.pop('tag')['name'])
        return AppliedTag.objects.create(tag=tag, **validated_data)


class SuggestedTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedTag
        fields = ['id', 'tag_id', 'tag_name', 'tag_number_of_uses',
                  'content_type', 'object_id', 'is_add']

    tag_id = serializers.IntegerField(source='tag.id', read_only=True)
    tag_name = serializers.CharField(max_length=255, source='tag.name')
    tag_number_of_uses = serializers.IntegerField(
        source='tag.number_of_uses', read_only=True)

    def create(self, validated_data):
        (tag, _) = Tag.objects.get_or_create(
            name=validated_data.pop('tag')['name'])
        return SuggestedTag.objects.create(tag=tag, **validated_data)
