from rest_framework.viewsets import ModelViewSet
from .serializers import *


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class PageReferencesFeatureViewSet(ModelViewSet):
    queryset = PageReferencesFeature.objects.all()
    serializer_class = PageReferencesFeatureSerializer


class PageReferenceViewSet(ModelViewSet):
    queryset = PageReference.objects.all()
    serializer_class = PageReferenceSerializer


class FeatureViewSet(ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class ContentViewSet(ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FinishedPageViewSet(ModelViewSet):
    queryset = FinishedPage.objects.all()
    serializer_class = FinishedPageSerializer
