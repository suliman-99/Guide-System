from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('voted-item', VotedItemViewSet)

urlpatterns = router.urls
