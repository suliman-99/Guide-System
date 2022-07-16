from rest_framework.viewsets import ModelViewSet
from .serializers import *


class VotedItemViewSet(ModelViewSet):
    queryset = VotedItem.objects.all()
    serializer_class = VotedItemSerializer
