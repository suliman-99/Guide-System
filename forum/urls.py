from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('forums', ForumViewSet, basename='forum')
router.register('replies', ReplyViewSet, basename='reply')

urlpatterns = router.urls
