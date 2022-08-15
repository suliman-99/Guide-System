from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from .serializers import *


def ensure_page_pk(kwargs, key):
    if kwargs.get(key) is not None and kwargs[key] == 'home-page':
        kwargs[key] = 1


class ContentViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ContentSerializer

    def get_queryset(self):
        ensure_page_pk(self.kwargs, 'page_pk')
        return Content.objects.filter(page_id=self.kwargs['page_pk'])

    def get_serializer_context(self):
        ensure_page_pk(self.kwargs, 'page_pk')
        if self.kwargs.get('page_pk', None) is not None:
            return {'page_id': self.kwargs['page_pk']}


class FeedbackViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        ensure_page_pk(self.kwargs, 'page_pk')
        return Feedback.objects.filter(page_id=self.kwargs['page_pk'])

    def get_serializer_context(self):
        ensure_page_pk(self.kwargs, 'page_pk')
        if self.kwargs.get('page_pk', None) is not None:
            return {'page_id': self.kwargs['page_pk']}


class FeatureViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = FeatureSerializer

    def get_queryset(self):
        ensure_page_pk(self.kwargs, 'page_pk')
        return Feature.objects.filter(page_id=self.kwargs['page_pk'])

    def get_serializer_context(self):
        ensure_page_pk(self.kwargs, 'page_pk')
        if self.kwargs.get('page_pk', None) is not None:
            return {'page_id': self.kwargs['page_pk']}


class ReferenceViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        ensure_page_pk(self.kwargs, 'page_pk')
        return Reference.objects \
            .filter(parent_id=self.kwargs['page_pk']) \
            .select_related('child') \
            .prefetch_related('features__feature') \
            .order_by('index')

    def get_serializer_context(self):
        ensure_page_pk(self.kwargs, 'page_pk')
        if self.kwargs.get('page_pk', None) is not None:
            return {'page_id': self.kwargs['page_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateReferenceSerializer
        return ReferenceSerializer

    def create(self, request, *args, **kwargs):
        ensure_page_pk(self.kwargs, 'page_pk')
        if self.kwargs['page_pk'] == request.data['child_id']:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        ensure_page_pk(self.kwargs, 'page_pk')
        instance = self.get_object()
        instance.delete()
        count = 0
        references = Reference.objects.filter(
            parent_id=kwargs['page_pk']).order_by('index')
        for reference in references:
            reference.index = count
            reference.save()
            count += 1
        Page.objects.filter(id=kwargs['page_pk']).update(
            reference_next_index=count)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_inedx(self, o):
        return o['index']

    @action(detail=False, methods=['get', 'post', 'delete'])
    def sort(self, request, page_pk):
        if page_pk == 'home-page':
            page_pk = 1
        data = request.data
        data.sort(key=self.get_inedx)
        is_valid = True
        count = 0
        for i in data:
            if i['index'] != count:
                is_valid = False
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            count += 1
        if count != Reference.objects.count():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if is_valid:
            for i in data:
                Reference.objects \
                    .filter(id=i['id']) \
                    .update(
                        index=i['index']+10000)
            for i in data:
                Reference.objects \
                    .filter(id=i['id']) \
                    .update(index=i['index'])
        Page.objects.filter(id=page_pk).update(reference_next_index=count)
        return Response(status=status.HTTP_202_ACCEPTED)


class DependencyViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        ensure_page_pk(self.kwargs, 'page_pk')
        return Dependency.objects.filter(parent_id=self.kwargs['page_pk']).select_related('child')

    def get_serializer_context(self):
        ensure_page_pk(self.kwargs, 'page_pk')
        if self.kwargs.get('page_pk', None) is not None:
            return {'page_id': self.kwargs['page_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateDependencySerializer
        return DependencySerializer


class ReferenceFeatureViewSet(ModelViewSet):
    http_method_names = ['get', 'patch']

    def get_queryset(self):
        ensure_page_pk(self.kwargs, 'page_pk')
        return ReferenceFeature.objects \
            .filter(reference_id=self.kwargs['reference_pk']) \
            .prefetch_related('feature')

    def get_serializer_context(self):
        if self.kwargs.get('reference_pk', None) is not None:
            return {'reference_id': self.kwargs['reference_pk']}

    def get_serializer_class(self):
        if self.request.method in ['PATCH']:
            return updateReferenceFeatureSerializer
        return ReferenceFeatureSerializer


class PageViewSet(ModelViewSet):

    def get_queryset(self):
        ensure_page_pk(self.kwargs, 'pk')
        if self.kwargs.get('pk') is not None:
            sorted_references = Reference.objects \
                .filter(parent_id=self.kwargs.get('pk')) \
                .select_related('child') \
                .prefetch_related('features__feature') \
                .order_by('index')
            prefetch = Prefetch('reference_children', queryset=sorted_references)
            return Page.objects \
                .prefetch_related('contents') \
                .prefetch_related('feedbacks') \
                .prefetch_related('features') \
                .prefetch_related('dependency_children__child') \
                .prefetch_related(prefetch) \
                .prefetch_related('finished_users__user')
        return Page.objects \
            .prefetch_related('contents') \
            .prefetch_related('feedbacks') \
            .prefetch_related('features') \
            .prefetch_related('dependency_children__child') \
            .prefetch_related('reference_children__child') \
            .prefetch_related('reference_children__features__feature') \
            .prefetch_related('finished_users__user')
            

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return SmallPageSerializer
        return PageSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def destroy(self, request, *args, **kwargs):
        ensure_page_pk(self.kwargs, 'pk')
        instance = self.get_object()
        if instance.id == 1:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'post', 'delete'])
    def mark_as_finished(self, request, pk):
        if pk == 'home-page' or int(pk) == 1:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user_id = request.user.id
        FinishedPage.objects.get_or_create(user_id=user_id, page_id=pk)
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get', 'post', 'delete'])
    def un_mark_as_finished(self, request, pk):
        if pk == 'home-page' or int(pk) == 1:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user_id = request.user.id
        finished_pages = FinishedPage.objects.filter(
            user_id=user_id, page_id=pk)
        if finished_pages:
            finished_page = finished_pages[0]
            finished_page.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
