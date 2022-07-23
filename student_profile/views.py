from rest_framework.viewsets import ModelViewSet

from student_profile.permissions import IsOwnerOrReadOnly
from .serializers import *
from rest_framework import permissions

class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(profile_id=self.kwargs['profile_pk'])

    def get_serializer_context(self):
        if not self.kwargs.get('profile_pk', None) is None:
            return {'profile_id': self.kwargs['profile_pk']}


class MarkViewSet(ModelViewSet):
    serializer_class = MarkSerializer

    def get_queryset(self):
        return Mark.objects.filter(profile_id=self.kwargs['profile_pk'])

    def get_serializer_context(self):
        if not self.kwargs.get('profile_pk', None) is None:
            return {'profile_id': self.kwargs['profile_pk']}


class ExperienceViewSet(ModelViewSet):
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        return Experience.objects.filter(profile_id=self.kwargs['profile_pk'])

    def get_serializer_context(self):
        if not self.kwargs.get('profile_pk', None) is None:
            return {'profile_id': self.kwargs['profile_pk']}


class ProfileMembershipViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Membership.objects.filter(profile_id=self.kwargs['profile_pk']).select_related('project')

    def get_serializer_context(self):
        if not self.kwargs.get('profile_pk', None) is None:
            return {'profile_id': self.kwargs['profile_pk']}

    def get_serializer_class(self):
        if not self.request is None:
            if self.request.method == 'POST':
                return CreateProfileMembershipSerializer
            elif self.request.method == 'PATCH':
                return updateProfileMembershipSerializer
        return ProfileMembershipSerializer


class ProjectMembershipViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Membership.objects.filter(project_id=self.kwargs['project_pk']).select_related('profile')

    def get_serializer_context(self):
        if not self.kwargs.get('project_pk', None) is None:
            return {'project_id': self.kwargs['project_pk']}

    def get_serializer_class(self):
        if not self.request is None:
            if self.request.method == 'POST':
                return CreateProjectMembershipSerializer
            elif self.request.method == 'PATCH':
                return updateProjectMembershipSerializer
        return ProjectMembershipSerializer


class ProfileViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Profile.objects \
        .select_related('user') \
        .prefetch_related('contacts') \
        .prefetch_related('marks') \
        .prefetch_related('experiences') \
        .prefetch_related('memberships__project')

    def get_serializer_context(self):
        if not self.request is None:
            if self.request.method == 'PATCH':
                if not self.kwargs.get('pk', None) is None:
                    return {'pk': self.kwargs['pk']}
        return {}

    def get_serializer_class(self):
        if not self.request is None:
            if self.request.method == 'POST':
                return CreateProfileSerializer
            elif self.request.method == 'PATCH':
                return UpdateProfileSerializer
        return ProfileSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.prefetch_related('memberships__profile')
    serializer_class = ProjectSerializer
