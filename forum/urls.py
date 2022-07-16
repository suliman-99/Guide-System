from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('forum', ForumViewSet)
router.register('reply', ReplyViewSet)

urlpatterns = router.urls
