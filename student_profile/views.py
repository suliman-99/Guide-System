from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


def ensure_profile_pk(kwargs, key, value):
    if kwargs.get(key) is not None and kwargs[key] == 'me':
        kwargs[key] = value


class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        ensure_profile_pk(self.kwargs, 'profile_pk', self.request.user.id)
        return Contact.objects.filter(profile_id=self.kwargs['profile_pk'])

    def get_serializer_context(self):
        ensure_profile_pk(self.kwargs, 'profile_pk', self.request.user.id)
        if self.kwargs.get('profile_pk', None) is not None:
            return {'profile_id': self.kwargs['profile_pk'], 'request': self.request}


class MarkViewSet(ModelViewSet):
    serializer_class = MarkSerializer

    def get_queryset(self):
        ensure_profile_pk(self.kwargs, 'profile_pk', self.request.user.id)
        return Mark.objects.filter(profile_id=self.kwargs['profile_pk'])

    def get_serializer_context(self):
        ensure_profile_pk(self.kwargs, 'profile_pk', self.request.user.id)
        if self.kwargs.get('profile_pk', None) is not None:
            return {'profile_id': self.kwargs['profile_pk'], 'request': self.request}


class ExperienceViewSet(ModelViewSet):
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        ensure_profile_pk(self.kwargs, 'profile_pk', self.request.user.id)
        return Experience.objects.filter(profile_id=self.kwargs['profile_pk'])

    def get_serializer_context(self):
        ensure_profile_pk(self.kwargs, 'profile_pk', self.request.user.id)
        if self.kwargs.get('profile_pk', None) is not None:
            return {'profile_id': self.kwargs['profile_pk'], 'request': self.request}


class ProfileToolViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = ProfileToolSerializer

    def get_queryset(self):
        ensure_profile_pk(self.kwargs, 'profile_pk', self.request.user.id)
        if self.queryset is None:
            profile = Profile.objects \
                .filter(pk=self.kwargs['profile_pk']) \
                .prefetch_related('memberships__project__features__feature_tools__tool__tool_features__feature') \
                .get()
            self.queryset = Tool.objects.get_profile_tools(profile)
        return self.queryset

    def retrieve(self, request, profile_pk, pk):
        for o in self.get_queryset():
            if int(o.pk) == int(pk):
                return Response(self.get_serializer(o).data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ProjectToolViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = ProjectToolSerializer

    def get_queryset(self):
        if self.queryset is None:
            project = Project.objects \
                .filter(pk=self.kwargs['project_pk']) \
                .prefetch_related('features__feature_tools__tool__tool_features__feature') \
                .get()
            self.queryset = Tool.objects.get_project_tools(project)
        return self.queryset

    def retrieve(self, request, project_pk, pk):
        for o in self.get_queryset():
            if int(o.pk) == int(pk):
                return Response(self.get_serializer(o).data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FeatureToolViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = FeatureToolSerializer

    def get_queryset(self):
        return FeatureTool.objects \
            .filter(feature_id=self.kwargs['feature_pk']) \
            .select_related('tool')

    def get_serializer_context(self):
        if self.kwargs.get('feature_pk', None) is not None:
            return {'feature_id': self.kwargs['feature_pk'], 'request': self.request}


class FeatureViewSet(ModelViewSet):
    serializer_class = FeatureSerializer

    def get_queryset(self):
        return Feature.objects \
            .filter(project_id=self.kwargs['project_pk']) \
            .prefetch_related('feature_tools__tool')

    def get_serializer_context(self):
        if self.kwargs.get('project_pk', None) is not None:
            return {'project_id': self.kwargs['project_pk'], 'request': self.request}


class ProjectMembershipRequestViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateMembershipRequestSerializer
        return ProjectMembershipRequestSerializer

    def get_queryset(self):
        return MembershipRequest.objects \
            .filter(project_id=self.kwargs['project_pk']) \
            .prefetch_related('profile__user')

    def get_serializer_context(self):
        if self.kwargs.get('project_pk', None) is not None:
            return {'project_id': self.kwargs['project_pk'], 'request': self.request}


class ProjectMembershipViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateMembershipSerializer
        return ProjectMembershipSerializer

    def get_queryset(self):
        return Membership.objects \
            .filter(project_id=self.kwargs['project_pk']) \
            .prefetch_related('profile__user')


class ProjectViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'delete']
    serializer_class = ProjectSerializer
    queryset = Project.objects \
        .prefetch_related('memberships__profile__user') \
        .prefetch_related('features__feature_tools__tool__tool_features__feature')


class ProfileMembershipRequestViewSet(ModelViewSet):
    http_method_names = ['get', 'delete']
    serializer_class = ProfileMembershipRequestSerializer

    def get_queryset(self):
        ensure_profile_pk(self.kwargs, 'profile_pk', self.request.user.id)
        return MembershipRequest.objects \
            .filter(profile_id=self.kwargs['profile_pk']) \
            .prefetch_related('project__memberships__profile__user') \
            .prefetch_related('project__features__feature_tools__tool__tool_features__feature')

    def get_serializer_context(self):
        ensure_profile_pk(self.kwargs, 'profile_pk', self.request.user.id)
        if self.kwargs.get('profile_pk', None) is not None:
            return {'profile_id': self.kwargs['profile_pk'], 'request': self.request}

    @action(detail=True, methods=['get', 'delete'])
    def accept(self, request, profile_pk, pk):
        membership_request = MembershipRequest.objects.get(pk=pk)
        if int(request.user.id) == int(profile_pk) and int(request.user.id) == int(membership_request.profile.pk):
            Membership.objects.create_or_update(
                profile=membership_request.profile,
                project=membership_request.project,
                position=membership_request.position,
                is_admin=membership_request.is_admin,
            )
            membership_request.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['get', 'delete'])
    def reject(self, request, profile_pk, pk):
        membership_request = MembershipRequest.objects.get(pk=pk)
        if int(request.user.id) == int(profile_pk) and int(request.user.id) == int(membership_request.profile.pk):
            membership_request.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProfileMembershipViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateMembershipSerializer
        return ProfileMembershipSerializer

    def get_queryset(self):
        ensure_profile_pk(self.kwargs, 'profile_pk', self.request.user.id)
        return Membership.objects \
            .filter(profile_id=self.kwargs['profile_pk']) \
            .prefetch_related('project__memberships__profile__user') \
            .prefetch_related('project__features__feature_tools__tool__tool_features__feature')

    def get_serializer_context(self):
        ensure_profile_pk(self.kwargs, 'profile_pk', self.request.user.id)
        if self.kwargs.get('profile_pk', None) is not None:
            return {'profile_id': self.kwargs['profile_pk'], 'request': self.request}


class ProfileViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        ensure_profile_pk(self.kwargs, 'pk', self.request.user.id)
        return Profile.objects \
            .select_related('user') \
            .prefetch_related('contacts') \
            .prefetch_related('marks') \
            .prefetch_related('experiences') \
            .prefetch_related('memberships__project__memberships__profile__user') \
            .prefetch_related('memberships__project__features__feature_tools__tool__tool_features__feature')

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
