from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tag')
router.register('tagged-items', TaggedItemViewSet, basename='tagged-item')
router.register('suggested-tags', SuggestedTagViewSet, basename='suggested-tag')

urlpatterns = router.urls
