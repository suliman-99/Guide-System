from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(
    'voted-items',
    VotedItemViewSet,
    basename='voted-items'
)

urlpatterns = router.urls + [
    path('object-vote-data/content-type=<content_type>/object-id=<object_id>/',
         get_object_vote_data),
]
