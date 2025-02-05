from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BloodGroupViewSet, UserProfileViewSet, UserViewSet

router = DefaultRouter()
router.register('bloodgroups', BloodGroupViewSet)
router.register('userprofiles', UserProfileViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]