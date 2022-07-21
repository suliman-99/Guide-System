from rest_framework.viewsets import ModelViewSet
from .serializers import *


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects \
        .prefetch_related('contacts') \
        .prefetch_related('marks') \
        .prefetch_related('experiences') \
        .prefetch_related('projects') \
        .prefetch_related('memberships') 
    serializer_class = ProfileSerializer


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class MarkViewSet(ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer


class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MembershipViewSet(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
