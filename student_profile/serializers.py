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


# ---------------------------------------------------------------------------------------------


class ProfileSmallFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'project', 'title', 'description',
                  'start_date', 'end_date']


class ProfileToolFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureTool
        fields = ['id', 'feature']

    feature = ProfileSmallFeatureSerializer(read_only=True)


class ProfileToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'title', 'tool_features']

    tool_features = ProfileToolFeatureSerializer(many=True, read_only=True)


# ----------------------------------------------------------------------------
class ProjectSmallFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title', 'description',
                  'start_date', 'end_date']


class ProjectToolFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureTool
        fields = ['id', 'feature']

    feature = ProjectSmallFeatureSerializer(read_only=True)


class ProjectToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'title', 'tool_features']

    tool_features = ProjectToolFeatureSerializer(many=True, read_only=True)

# ----------------------------------------------------------------------------


class SmallToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'title']


class FeatureToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureTool
        fields = ['id', 'tool', 'tool_title']

    tool = SmallToolSerializer(read_only=True)
    tool_title = serializers.CharField(write_only=True)

    def create(self, validated_data):
        feature_id = self.context['feature_id']
        (tool, _) = Tool.objects.get_or_create(
            title=validated_data.pop('tool_title'))
        return FeatureTool.objects.create(feature_id=feature_id, tool=tool, **validated_data)


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title', 'description',
                  'start_date', 'end_date', 'feature_tools']

    feature_tools = FeatureToolSerializer(many=True, read_only=True)

    def create(self, validated_data):
        project_id = self.context['project_id']
        return Feature.objects.create(project_id=project_id, **validated_data)


# ---------------------------------------------------------------------------------------------

class UpdateMembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = ['position', 'is_admin']


class UpdateMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['position', 'is_admin']


class SmallProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'username', 'gender', 'photo']

    username = serializers.CharField(source='user.username')


class ProjectMembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = ['id', 'position', 'is_admin',
                  'time', 'profile_id', 'profile']

    profile_id = serializers.IntegerField(write_only=True)
    profile = SmallProfileSerializer(read_only=True)
    time = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        project_id = self.context['project_id']
        return MembershipRequest.objects.create(project_id=project_id, **validated_data)


class ProjectMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'position', 'is_admin',  'profile_id', 'profile']

    profile_id = serializers.IntegerField(write_only=True)
    profile = SmallProfileSerializer(read_only=True)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description',  'link', 'photo',
                  'is_certified', 'start_date', 'end_date', 'memberships', 'features', 'tools']

    features = FeatureSerializer(many=True, read_only=True)
    memberships = ProjectMembershipSerializer(many=True, read_only=True)
    tools = serializers.SerializerMethodField()

    def get_tools(self, project):
        return ProjectToolSerializer(Tool.objects.get_project_tools(project), many=True).data


class ProfileMembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = ['id', 'position', 'is_admin', 'time', 'project']

    project = ProjectSerializer()


class ProfileMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'position', 'is_admin', 'project']

    project = ProjectSerializer()
    is_admin = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        profile_id = self.context['profile_id']
        project = Project.objects.create(**validated_data.pop('project'))
        return Membership.objects.create(profile_id=profile_id, project=project, is_admin=True, **validated_data)


# ---------------------------------------------------------------------------------


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'gender', 'photo', 'address', 'services',
                  'preferences', 'birth_date', 'is_graduated', 'start_date', 'graduate_date', 'public_link', 'points', 'contacts', 'marks', 'experiences', 'memberships', 'tools']

    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    contacts = ContactSerializer(many=True, read_only=True)
    marks = MarkSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    memberships = ProfileMembershipSerializer(many=True, read_only=True)
    is_graduated = serializers.SerializerMethodField()
    public_link = serializers.SerializerMethodField()
    tools = serializers.SerializerMethodField()

    def get_tools(self, profile):
        return ProfileToolSerializer(Tool.objects.get_profile_tools(profile), many=True).data

    def get_is_graduated(self, profile):
        return profile.graduate_date is not None and profile.graduate_date < datetime.date(datetime.now())

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
