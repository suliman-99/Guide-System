from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class VotedItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = VotedItem.objects.all()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'request': self.request}

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateVotedItemSerializer
        return VotedItemSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id == instance.user.id:
            vote.send_robust(self.__class__, old_instance=instance,
                             new_instance=None)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id == instance.user.id:
            return super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_object_vote_data(request, content_type, object_id):
    return Response(VotedItem.objects.get_object_vote_data(
        content_type,
        object_id,
        request.user.id
    ))
