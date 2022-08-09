from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()

router.register(
    'profiles',
    ProfileViewSet,
    basename='profiles'
)

router.register(
    'projects',
    ProjectViewSet,
    basename='projects'
)

# --------------------------------------------------------------------------

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
    'memberships',
    ProfileMembershipViewSet,
    basename='profile-memberships'
)

profile_router.register(
    'membership-requests',
    ProfileMembershipRequestViewSet,
    basename='profile-membership-requests'
)

profile_router.register(
    'tools',
    ProfileToolViewSet,
    basename='profile-tools'
)

# --------------------------------------------------------------------------


project_router = routers.NestedDefaultRouter(
    router,
    'projects',
    lookup='project'
)

project_router.register(
    'memberships',
    ProjectMembershipViewSet,
    basename='project-memberships'
)

project_router.register(
    'membership-requests',
    ProjectMembershipRequestViewSet,
    basename='project-membership-requests'
)

project_router.register(
    'features',
    FeatureViewSet,
    basename='project-features'
)

project_router.register(
    'tools',
    ProjectToolViewSet,
    basename='project-tools'
)

# --------------------------------------------------------------------------


project_features_router = routers.NestedDefaultRouter(
    project_router,
    'features',
    lookup='feature'
)

project_features_router.register(
    'tools',
    FeatureToolViewSet,
    basename='project-feature-tools'
)

# --------------------------------------------------------------------------

urlpatterns = router.urls + profile_router.urls + \
    project_router.urls + project_features_router.urls
