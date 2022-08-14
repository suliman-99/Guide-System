from rest_framework import serializers
from .models import *


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


class SmallPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'type', 'background', 'icon',
                  'importance_and_advantages', 'advice_and_tools']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name']

    def create(self, validated_data):
        page_id = self.context['page_id']
        feature = Feature.objects.create(page_id=page_id, **validated_data)
        references = Reference.objects.filter(parent_id=page_id)
        for reference in references:
            ReferenceFeature.objects.create(
                reference=reference, feature=feature, value='')
        return feature


class ReferenceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceFeature
        fields = ['id', 'value', 'feature']

    feature = FeatureSerializer(read_only=True, many=False)


class updateReferenceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceFeature
        fields = ['value']


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['id', 'index', 'child', 'features']

    child = SmallPageSerializer(read_only=True)
    features = ReferenceFeatureSerializer(many=True, read_only=True)


class CreateReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['child_id']

    child_id = serializers.IntegerField()

    def create(self, validated_data):
        page_id = self.context['page_id']
        page = Page.objects.get(id=page_id)
        index = page.reference_next_index
        page.reference_next_index = index + 1
        page.save()
        reference = Reference.objects.create(
            parent_id=page_id, index=index, **validated_data)
        features = Feature.objects.filter(page_id=page_id)
        for feature in features:
            ReferenceFeature.objects.create(
                reference=reference, feature=feature, value='')
        return reference


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
        fields = ['id', 'title', 'type', 'background', 'icon',
                  'importance_and_advantages', 'advice_and_tools', 'is_finished', 'contents', 'feedbacks',  'features', 'dependency_children', 'reference_children']

    contents = ContentSerializer(many=True, read_only=True)
    feedbacks = FeedbackSerializer(many=True, read_only=True)

    features = FeatureSerializer(many=True, read_only=True)
    dependency_children = DependencySerializer(many=True, read_only=True)
    reference_children = ReferenceSerializer(many=True, read_only=True)

    is_finished = serializers.SerializerMethodField()

    def get_is_finished(self, page):
        if self.context['user_id'] in [p.user.id for p in page.finished_users.all()]:
            return True
        return False
