from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profile')
router.register('contacts', ContactViewSet, basename='contact')
router.register('marks', MarkViewSet, basename='mark')
router.register('experiences', ExperienceViewSet, basename='experience')
router.register('projects', ProjectViewSet, basename='project')
router.register('memberships', MembershipViewSet, basename='membership')

urlpatterns = router.urls
