from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('profile', ProfileViewSet)
router.register('contact', ContactViewSet)
router.register('mark', MarkViewSet)
router.register('experience', ExperienceViewSet)
router.register('project', ProjectViewSet)
router.register('membership', MembershipViewSet)

urlpatterns = router.urls
