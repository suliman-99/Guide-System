from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()

router.register(
    'pages',
    PageViewSet,
    basename='pages'
)

# --------------------------------------------------------------------------

page_router = routers.NestedDefaultRouter(
    router,
    'pages',
    lookup='page'
)

page_router.register(
    'contents',
    ContentViewSet,
    basename='page-contents'
)
page_router.register(
    'feedbacks',
    FeedbackViewSet,
    basename='page-feedbacks'
)
page_router.register(
    'features',
    FeatureViewSet,
    basename='page-features'
)
page_router.register(
    'references',
    ReferenceViewSet,
    basename='page-references'
)
page_router.register(
    'dependencies',
    DependencyViewSet,
    basename='page-dependencies'
)

# --------------------------------------------------------------------------

page_reference_router = routers.NestedDefaultRouter(
    page_router,
    'references',
    lookup='reference'
)

page_reference_router.register(
    'features',
    ReferenceFeatureViewSet,
    basename='page-reference-features'
)

# --------------------------------------------------------------------------

urlpatterns = router.urls + page_router.urls + page_reference_router.urls
