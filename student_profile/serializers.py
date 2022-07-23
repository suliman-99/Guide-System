from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    # experience_set = serializers.StringRelatedField(many=True)
    project_set = serializers.StringRelatedField(many=True)
    experience_set = serializers.SerializerMethodField()

    def get_experience_set(self, experience):
        return experience.experience_set.values_list('name', flat=True)
    
    class Meta:
        model = Profile
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Experience
        fields = ['profile', 'name', 'owner', 'is_certified']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'
