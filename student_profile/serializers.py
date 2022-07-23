from typing_extensions import Required
from django.shortcuts import get_object_or_404
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


class SmallProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'link',
                  'is_cerified', 'start_date', 'end_date']


class SmallProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'gender', 'points', 'photo', 'address', 'services',
                  'preferences', 'birth_date', 'is_graduated', 'start_date', 'end_date']

    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')


class ProfileMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'position', 'project']

    project = SmallProjectSerializer()


class CreateProfileMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['position', 'project_id']

    project_id = serializers.IntegerField()

    def create(self, validated_data):
        profile_id = self.context['profile_id']
        return Membership.objects.create(profile_id=profile_id, **validated_data)


class updateProfileMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['position']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'gender', 'points', 'photo', 'address', 'services',
                  'preferences', 'birth_date', 'is_graduated', 'start_date', 'end_date', 'contacts', 'marks', 'experiences', 'memberships']

    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    contacts = ContactSerializer(many=True, read_only=True)
    marks = MarkSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    memberships = ProfileMembershipSerializer(many=True, read_only=True)


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'gender', 'points', 'photo', 'address', 'services',
                  'preferences', 'birth_date', 'is_graduated', 'start_date', 'end_date']

    user_id = serializers.IntegerField()


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'points', 'photo', 'address', 'services',
                  'preferences', 'birth_date', 'is_graduated', 'start_date', 'end_date']

    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    def update(self, instance, validated_data):
        user = get_object_or_404(User, pk=self.context['pk'])
        data = validated_data.pop('user')
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()
        instance.user = user
        return super().update(instance, validated_data)


class ProjectMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'position', 'profile']

    profile = SmallProfileSerializer()


class CreateProjectMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['position', 'profile_id']

    profile_id = serializers.IntegerField()

    def create(self, validated_data):
        project_id = self.context['project_id']
        return Membership.objects.create(project_id=project_id, **validated_data)


class updateProjectMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['position']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'link',
                  'is_cerified', 'start_date', 'end_date', 'memberships']

    memberships = ProjectMembershipSerializer(many=True, read_only=True)
