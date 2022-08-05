from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(
    'tags',
    TagViewSet,
    basename='tags'
)
router.register(
    'applied-tags',
    AppliedTagViewSet,
    basename='applied-tags'
)
router.register(
    'suggested-tags',
    SuggestedTagViewSet,
    basename='suggested-tags'
)

urlpatterns = router.urls + [
    path('applied-tags/content-type=<content_type>/object-id=<object_id>/',
         get_object_Applied_tags),
    path('suggested-tags/content-type=<content_type>/object-id=<object_id>/',
         get_object_suggested_tags)
]
