from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from apps.pecs.views.collection_view import CollectionView
from apps.pecs.views.pictogram_usage_view import PictogramUsageView
from apps.pecs.views.pictogram_view import PictogramCollectionView, PictogramView


router = DefaultRouter()

router.register(r"collections", CollectionView, basename="collection")
router.register(r"pictograms", PictogramView, basename="pictogram")
router.register(r"pictograms-usage", PictogramUsageView, basename="pictogram-usage")

collections_router = NestedSimpleRouter(router, r"collections", lookup="collection")
collections_router.register(r"pictograms", PictogramCollectionView, basename="collection-pictograms")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(collections_router.urls)),
]