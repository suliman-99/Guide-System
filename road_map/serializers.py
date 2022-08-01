from attr import validate
from rest_framework import serializers
from .models import *


class SmallPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'type', 'background', 'icon', 'view_template',
                  'importance_and_advantages', 'advice_and_tools']


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'content', 'link']

    def create(self, validated_data):
        page_id = self.context['page_id']
        return Content.objects.create(page_id=page_id, **validated_data)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'content']

    def create(self, validated_data):
        page_id = self.context['page_id']
        return Feedback.objects.create(page_id=page_id, **validated_data)


class FinishedPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedPage
        fields = ['id', 'user']

    def create(self, validated_data):
        page_id = self.context['page_id']
        return FinishedPage.objects.create(page_id=page_id, **validated_data)


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name']

    def create(self, validated_data):
        page_id = self.context['page_id']
        return Feature.objects.create(page_id=page_id, **validated_data)


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['id', 'child', 'index', 'features']

    child = SmallPageSerializer(read_only=True)
    features = FeatureSerializer(many=True, read_only=True)


class CreateReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['child_id', 'index']

    child_id = serializers.IntegerField()

    def create(self, validated_data):
        page_id = self.context['page_id']
        return Reference.objects.create(parent_id=page_id, **validated_data)


class ReferenceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceFeature
        fields = ['id', 'reference', 'feature', 'value']


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = ['id', 'child']

    child = SmallPageSerializer(read_only=True)


class CreateDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = ['child_id']

    child_id = serializers.IntegerField()

    def create(self, validated_data):
        page_id = self.context['page_id']
        return Dependency.objects.create(parent_id=page_id, **validated_data)


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'type', 'background', 'icon', 'view_template',
                  'importance_and_advantages', 'advice_and_tools', 'contents', 'feedbacks', 'finished_users', 'dependency_children', 'reference_children', 'features']

    contents = ContentSerializer(many=True, read_only=True)
    feedbacks = FeedbackSerializer(many=True, read_only=True)
    finished_users = FinishedPageSerializer(many=True, read_only=True)

    dependency_children = DependencySerializer(many=True, read_only=True)
    reference_children = ReferenceSerializer(many=True, read_only=True)
    features = FeatureSerializer(many=True, read_only=True)
