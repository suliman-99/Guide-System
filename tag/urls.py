from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('tag', TagViewSet)
router.register('tagged-item', TaggedItemViewSet)
router.register('suggested-tag', SuggestedTagViewSet)

urlpatterns = router.urls
