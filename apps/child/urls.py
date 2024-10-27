from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from apps.child.views.child_view import ChildViewSet
from apps.child.views.collection_view import CollectionView
from apps.child.views.pictogram_view import PictogramView

router = DefaultRouter()
router.register(r"children", ChildViewSet, basename="child")
router.register(r"collections", CollectionView, basename="collection")
router.register(r"pictograms", PictogramView, basename="pictogram")

urlpatterns = [
    path("", include(router.urls)),
]
