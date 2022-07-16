from rest_framework import serializers
from .models import *


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class PageReferencesFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageReferencesFeature
        fields = '__all__'


class PageReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageReference
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class FinishedPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedPage
        fields = '__all__'
