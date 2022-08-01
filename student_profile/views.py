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


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.kwargs['profile_pk'] == 'me':
            self.kwargs['profile_pk'] = self.request.user.id
        return Project.objects.filter(profile_id=self.kwargs['profile_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('profile_pk', None) is not None:
            return {'profile_id': self.kwargs['profile_pk']}


class ProfileViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    queryset = Profile.objects \
        .select_related('user') \
        .prefetch_related('contacts') \
        .prefetch_related('marks') \
        .prefetch_related('experiences') \
        .prefetch_related('projects')

    def get_queryset(self):
        if self.kwargs.get('pk', None) == 'me':
            self.kwargs['pk'] = self.request.user.id
        return Profile.objects \
            .select_related('user') \
            .prefetch_related('contacts') \
            .prefetch_related('marks') \
            .prefetch_related('experiences') \
            .prefetch_related('projects')

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
