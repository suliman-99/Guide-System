from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('page', PageViewSet)
router.register('page-references-feature', PageReferencesFeatureViewSet)
router.register('page-reference', PageReferenceViewSet)
router.register('feature', FeatureViewSet)
router.register('content', ContentViewSet)
router.register('feedback', FeedbackViewSet)
router.register('finished-page', FinishedPageViewSet)

urlpatterns = router.urls
