from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class TagViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AppliedTagViewSet(ModelViewSet):
    http_method_names = ['post', 'delete']
    queryset = AppliedTag.objects.all()
    serializer_class = AppliedTagSerializer


class SuggestedTagViewSet(ModelViewSet):
    http_method_names = ['post', 'delete']
    queryset = SuggestedTag.objects.all()
    serializer_class = SuggestedTagSerializer

    @action(detail=True, methods=['delete'])
    def accept(self, request, pk):
        suggested_tag = SuggestedTag.objects.get(pk=pk)
        if suggested_tag.is_add:
            AppliedTag.objects.get_or_create(
                tag=suggested_tag.tag, content_type=suggested_tag.content_type, object_id=suggested_tag.object_id)
        else:
            tagged_item = AppliedTag.objects.get(
                tag=suggested_tag.tag, content_type=suggested_tag.content_type, object_id=suggested_tag.object_id)
            tagged_item.delete()
        suggested_tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['delete'])
    def reject(self, request, pk):
        suggested_tag = SuggestedTag.objects.get(pk=pk)
        suggested_tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_object_Applied_tags(request, content_type, object_id):
    return Response(AppliedTagSerializer(AppliedTag.objects.get_object_tags(
        content_type,
        object_id,
    ),
        many=True,
    ).data)


@api_view(['GET'])
def get_object_suggested_tags(request, content_type, object_id):
    return Response(SuggestedTagSerializer(SuggestedTag.objects.get_object_tags(
        content_type,
        object_id,
    ),
        many=True,
    ).data)
