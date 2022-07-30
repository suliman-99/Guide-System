from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .serializers import *


class ReplyViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Reply.objects.filter(forum_id=self.kwargs['forum_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('forum_pk', None) is not None:
            return {'user_id': self.request.user.id, 'forum_id': self.kwargs['forum_pk']}

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return CreateReplySerializer
        return ReplySerializer

    @action(detail=True, methods=['GET'])
    def close(self, request, forum_pk, pk):
        forum = Forum.objects.get(pk=forum_pk)
        if forum.user_id == request.user.id:
            reply = Reply.objects.get(pk=pk)
            forum.closed_reply = reply
            forum.save()
            return Response()


class ForumViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    queryset = Forum.objects.prefetch_related('replies')

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return CreateForumSerializer
        return ForumSerializer
