from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('pages', PageViewSet, basename='pages')
router.register('page-references-features', PageReferencesFeatureViewSet, basename='page-references-feature')
router.register('page-references', PageReferenceViewSet, basename='page-reference')
router.register('features', FeatureViewSet, basename='feature')
router.register('contents', ContentViewSet, basename='content')
router.register('feedbacks', FeedbackViewSet, basename='feedback')
router.register('finished-pages', FinishedPageViewSet, basename='finished-page')

urlpatterns = router.urls
