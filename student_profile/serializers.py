from rest_framework import serializers
from .models import *



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many= True, read_only=True)
    marks = MarkSerializer(many= True, read_only=True)
    experiences = ExperienceSerializer(many= True, read_only=True)
    projects = ProjectSerializer(many= True, read_only=True)
    memberships = MembershipSerializer(many= True, read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

