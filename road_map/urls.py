from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()
router.register('pages', PageViewSet, basename='pages')
router.register('page-references-features',
                FeatureViewSet, basename='page-references-feature')
router.register('page-references', ReferenceViewSet,
                basename='page-reference')
router.register('features', ReferenceFeatureViewSet, basename='feature')

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
    'finished-users',
    FinishedPageViewSet,
    basename='page-finished-users'
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


urlpatterns = router.urls + page_router.urls
