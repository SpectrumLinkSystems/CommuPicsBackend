from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import TherapistViewSet
from apps.child.views.child_view import ChildViewSet, TherapistChildViewSet

router = DefaultRouter()
router.register(r'therapists', TherapistViewSet, basename='therapists')

therapists_router = NestedDefaultRouter(router, r'therapists', lookup='therapist')
therapists_router.register(r'children', TherapistChildViewSet, basename='therapist-children')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(therapists_router.urls)),
    path('therapists/<int:pk>/child_tracking/', TherapistViewSet.as_view({'post': 'child_tracking'}), name='child_tracking'),
]