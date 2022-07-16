from rest_framework import serializers
from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TaggedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaggedItem
        fields = '__all__'


class SuggestedTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedTag
        fields = '__all__'
