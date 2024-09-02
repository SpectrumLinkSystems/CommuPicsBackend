from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.views import ProfileChildViewSet, ProfileParentViewSet, ProfileTherapistViewSet

router = DefaultRouter()
router.register(r'children', ProfileChildViewSet)
router.register(r'parents', ProfileParentViewSet)
router.register(r'therapists', ProfileTherapistViewSet)

urlpatterns = [
    path('', include(router.urls)),
]