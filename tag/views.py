from rest_framework.viewsets import ModelViewSet
from .serializers import *


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TaggedItemViewSet(ModelViewSet):
    queryset = TaggedItem.objects.all()
    serializer_class = TaggedItemSerializer


class SuggestedTagViewSet(ModelViewSet):
    queryset = SuggestedTag.objects.all()
    serializer_class = SuggestedTagSerializer
