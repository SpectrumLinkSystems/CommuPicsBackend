from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from apps.child.views.child_view import ChildViewSet
from apps.pecs.views.collection_view import CollectionView 
from apps.pecs.views.pictogram_view import PictogramView
from apps.pecs.views.pictogram_usage_view import PictogramUsageView
from apps.recomendation.recomendation_view import RecomendationView

router = DefaultRouter()
router.register(r"children", ChildViewSet, basename="child")
router.register(r"collections", CollectionView, basename="collection")
router.register(r"pictograms", PictogramView, basename="pictogram")
router.register(r"history", PictogramUsageView, basename="history")
router.register(r"recomendation", RecomendationView, basename="recomendation")

urlpatterns = [
    path("", include(router.urls)),
]

