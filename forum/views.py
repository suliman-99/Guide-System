from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from forum.filters import ForumFilter
from forum.pagination import PageNumberPagination10
from .serializers import *


class ReplyViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination10

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
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ForumViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination10
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']
    ordering_fields = ['time']
    filterset_class = ForumFilter

    queryset = Forum.objects.all()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return CreateForumSerializer
        return ForumSerializer
