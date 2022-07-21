from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('voted-items', VotedItemViewSet, basename='voted-item')

urlpatterns = router.urls
