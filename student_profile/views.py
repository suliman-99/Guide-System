from pprint import pprint
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *


class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        if self.kwargs['profile_pk'] == 'me':
            self.kwargs['profile_pk'] = self.request.user.id
        return Contact.objects.filter(profile_id=self.kwargs['profile_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('profile_pk', None) is not None:
            return {'profile_id': self.kwargs['profile_pk']}


class MarkViewSet(ModelViewSet):
    serializer_class = MarkSerializer

    def get_queryset(self):
        if self.kwargs['profile_pk'] == 'me':
            self.kwargs['profile_pk'] = self.request.user.id
        return Mark.objects.filter(profile_id=self.kwargs['profile_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('profile_pk', None) is not None:
            return {'profile_id': self.kwargs['profile_pk']}


class ExperienceViewSet(ModelViewSet):
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        if self.kwargs['profile_pk'] == 'me':
            self.kwargs['profile_pk'] = self.request.user.id
        return Experience.objects.filter(profile_id=self.kwargs['profile_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('profile_pk', None) is not None:
            return {'profile_id': self.kwargs['profile_pk']}


class ProfileMembershipViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        if self.kwargs['profile_pk'] == 'me':
            self.kwargs['profile_pk'] = self.request.user.id
        return Membership.objects.filter(profile_id=self.kwargs['profile_pk']).select_related('project')

    def get_serializer_context(self):
        if self.kwargs.get('profile_pk', None) is not None:
            return {'profile_id': self.kwargs['profile_pk']}

    def get_serializer_class(self):
        if self.request is not None:
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
        if self.kwargs.get('project_pk', None) is not None:
            return {'project_id': self.kwargs['project_pk'], 'request': self.request}

    def get_serializer_class(self):
        if self.request is not None:
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

    def get_queryset(self):
        if self.kwargs.get('pk', None) == 'me':
            self.kwargs['pk'] = self.request.user.id
        return Profile.objects \
            .select_related('user') \
            .prefetch_related('contacts') \
            .prefetch_related('marks') \
            .prefetch_related('experiences') \
            .prefetch_related('memberships__project')

    def get_serializer_class(self):
        if self.request is not None:
            if self.request.method == 'POST':
                return CreateProfileSerializer
            elif self.request.method == 'PATCH':
                return UpdateProfileSerializer
        return ProfileSerializer

    def get_serializer_context(self):
        if self.request is not None:
            return {'request': self.request}
        return {}

    @action(detail=False, permission_classes=[IsAuthenticated], methods=['Get'])
    def get_public_link(self, request):
        profile = Profile.objects.get(user_id=request.user.id)
        return Response({'public_link': profile.get_public_link(request)})

    # @action(detail=False, permission_classes=[IsAuthenticated], methods=['Get', 'PATCH'])
    # def me(self, request):
    #     profile = Profile.objects \
    #         .filter(user_id=request.user.id) \
    #         .select_related('user') \
    #         .prefetch_related('contacts') \
    #         .prefetch_related('marks') \
    #         .prefetch_related('experiences') \
    #         .prefetch_related('memberships__project') \
    #         .get()
    #     if request.method == 'GET':
    #         serializer = ProfileSerializer(
    #             profile, context=self.get_serializer_context())
    #         return Response(serializer.data)
    #     elif request.method == 'PATCH':
    #         serializer = UpdateProfileSerializer(
    #             profile, data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)


class ProjectViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Project.objects.prefetch_related('memberships__profile')

    def get_serializer_class(self):
        if self.request is not None:
            if self.request.method in ['POST', 'PATCH']:
                return CreateProjectSerializer
        return ProjectSerializer
