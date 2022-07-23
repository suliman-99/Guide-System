from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()
router.register('profiles', ProfileViewSet)
router.register('projects', ProjectViewSet)

profile_router = routers.NestedDefaultRouter(
    router,
    'profiles',
    lookup='profile'
)
Project_router = routers.NestedDefaultRouter(
    router,
    'projects',
    lookup='project'
)

profile_router.register(
    'memberships',
    ProfileMembershipViewSet,
    basename='profile-memberships'
)
Project_router.register(
    'memberships',
    ProjectMembershipViewSet,
    basename='project-memberships'
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

urlpatterns = router.urls + profile_router.urls + Project_router.urls
