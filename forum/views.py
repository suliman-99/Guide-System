from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from forum.filters import ForumFilter
from forum.pagination import PageNumberPagination10
from .serializers import *
from .signals import *


class ReplyViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination10
    filter_backends = [OrderingFilter]
    ordering_fields = ['time', 'points']

    def get_queryset(self):
        return Reply.objects.filter(forum_id=self.kwargs['forum_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('forum_pk', None) is not None:
            return {'user_id': self.request.user.id, 'forum_id': self.kwargs['forum_pk']}

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return CreateReplySerializer
        return ReplySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.closed_forum is not None:
            forum_close.send_robust(
                self.__class__, old_reply=instance, new_reply=None)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'post', 'delete'])
    def close(self, request, forum_pk, pk):
        reply = Reply.objects.get(pk=pk)
        forum = reply.forum
        if int(forum.user_id) == int(request.user.id) and int(forum.id) == int(forum_pk):
            forum_close.send_robust(
                self.__class__, old_reply=forum.closed_reply, new_reply=reply)
            forum.closed_reply = reply
            forum.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ForumViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination10
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']
    ordering_fields = ['time', 'points']
    filterset_class = ForumFilter

    queryset = Forum.objects.all()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return CreateForumSerializer
        return ForumSerializer

    @action(detail=True, methods=['get', 'post', 'delete'])
    def un_close(self, request, pk):
        forum = Forum.objects.get(pk=pk)
        if int(forum.user_id) == int(request.user.id):
            forum_close.send_robust(
                self.__class__, old_reply=forum.closed_reply, new_reply=None)
            forum.closed_reply = None
            forum.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
