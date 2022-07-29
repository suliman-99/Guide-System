# from typing_extensions import Required
from datetime import datetime
from rest_framework import serializers
from .models import *


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'type', 'link']

    def create(self, validated_data):
        profile_id = self.context['profile_id']
        return Contact.objects.create(profile_id=profile_id, **validated_data)


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['id', 'subject_name', 'mark', 'date']

    def create(self, validated_data):
        profile_id = self.context['profile_id']
        return Mark.objects.create(profile_id=profile_id, **validated_data)


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'name', 'type', 'description',
                  'start_date', 'end_date', 'is_certified']

    def create(self, validated_data):
        profile_id = self.context['profile_id']
        return Experience.objects.create(profile_id=profile_id, **validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'position',  'link',
                  'is_cerified', 'start_date', 'end_date']

    def create(self, validated_data):
        profile_id = self.context['profile_id']
        return Project.objects.create(profile_id=profile_id, **validated_data)


# ---------------------------------------------------------------------------------


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'gender', 'points', 'photo', 'address', 'services',
                  'preferences', 'birth_date', 'is_graduated', 'start_date', 'graduate_date', 'public_link', 'contacts', 'marks', 'experiences', 'projects']

    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    contacts = ContactSerializer(many=True, read_only=True)
    marks = MarkSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    is_graduated = serializers.SerializerMethodField()
    public_link = serializers.SerializerMethodField()

    def get_is_graduated(self, profile):
        return profile.graduate_date is not None and profile.graduate_date < datetime.now()

    def get_public_link(self, profile):
        return profile.get_public_link(self.context['request'])


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'gender', 'photo', 'address', 'services',
                  'preferences', 'birth_date', 'start_date', 'graduate_date']

    user_id = serializers.IntegerField()


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'photo', 'address', 'services',
                  'preferences', 'birth_date', 'start_date', 'graduate_date']

    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    def update(self, instance, validated_data):
        data = validated_data.pop('user')
        user = instance.user
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()
        instance.user = user
        return super().update(instance, validated_data)
