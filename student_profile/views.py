from rest_framework.viewsets import ModelViewSet

from student_profile.permissions import IsOwnerOrReadOnly
from .serializers import *
from rest_framework import permissions

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
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

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MembershipViewSet(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
