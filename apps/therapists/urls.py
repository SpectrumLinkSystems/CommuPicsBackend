from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TherapistViewSet

router = DefaultRouter()
router.register(r'therapists', TherapistViewSet, basename='therapists')

urlpatterns = [
    path('', include(router.urls)),
]