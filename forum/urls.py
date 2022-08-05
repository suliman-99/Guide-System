from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()
router.register(
    'forums',
    ForumViewSet,
    basename='forums'
)

forum_router = routers.NestedDefaultRouter(
    router,
    'forums',
    lookup='forum'
)

forum_router.register(
    'replies',
    ReplyViewSet,
    basename='forum-replies'
)

urlpatterns = router.urls + forum_router.urls
