from rest_framework.viewsets import ModelViewSet
from .serializers import *


class ContentViewSet(ModelViewSet):
    serializer_class = ContentSerializer

    def get_queryset(self):
        return Content.objects.filter(page_id=self.kwargs['page_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('page_pk', None) is not None:
            return {'page_id': self.kwargs['page_pk']}


class FeedbackViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return Feedback.objects.filter(page_id=self.kwargs['page_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('page_pk', None) is not None:
            return {'page_id': self.kwargs['page_pk']}


class FinishedPageViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = FinishedPageSerializer

    def get_queryset(self):
        return FinishedPage.objects.filter(page_id=self.kwargs['page_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('page_pk', None) is not None:
            return {'page_id': self.kwargs['page_pk']}


class FeatureViewSet(ModelViewSet):
    serializer_class = FeatureSerializer

    def get_queryset(self):
        return Feature.objects.filter(page_id=self.kwargs['page_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('page_pk', None) is not None:
            return {'page_id': self.kwargs['page_pk']}


class ReferenceViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Reference.objects.filter(parent_id=self.kwargs['page_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('page_pk', None) is not None:
            return {'page_id': self.kwargs['page_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateReferenceSerializer
        return ReferenceSerializer


class DependencyViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Dependency.objects.filter(parent_id=self.kwargs['page_pk'])

    def get_serializer_context(self):
        if self.kwargs.get('page_pk', None) is not None:
            return {'page_id': self.kwargs['page_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateDependencySerializer
        return DependencySerializer


class ReferenceFeatureViewSet(ModelViewSet):
    queryset = ReferenceFeature.objects.all()
    serializer_class = ReferenceFeatureSerializer


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return SmallPageSerializer
        return PageSerializer
