from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import TherapistViewSet
from apps.child.views.child_view import ChildViewSet

router = DefaultRouter()
router.register(r'therapists', TherapistViewSet, basename='therapists')

therapists_router = NestedDefaultRouter(router, r'therapists', lookup='therapist')
therapists_router.register(r'children', ChildViewSet, basename='therapist-children')

urlpatterns = [
    path('therapists/<int:pk>/assign-child/', 
         TherapistViewSet.as_view({'post': 'assign_child'}),
         name='therapist-assign-child'),
] + router.urls