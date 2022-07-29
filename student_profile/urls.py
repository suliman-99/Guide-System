from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()
router.register('profiles', ProfileViewSet)

profile_router = routers.NestedDefaultRouter(
    router,
    'profiles',
    lookup='profile'
)

profile_router.register(
    'contacts',
    ContactViewSet,
    basename='profile-contacts'
)
profile_router.register(
    'marks',
    MarkViewSet,
    basename='profile-marks'
)
profile_router.register(
    'experiences',
    ExperienceViewSet,
    basename='profile-experiences'
)

profile_router.register(
    'projects',
    ProjectViewSet,
    basename='profile-projects'
)

urlpatterns = router.urls + profile_router.urls
