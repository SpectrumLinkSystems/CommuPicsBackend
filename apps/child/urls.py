from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from apps.child.views.child_view import ChildViewSet
from apps.pecs.views.collection_view import CollectionChildView 
from apps.pecs.views.pictogram_usage_view import PictogramUsageView, UsageChildView
from apps.child.views.recomendation_view import RecomendationView

router = DefaultRouter()
router.register(r"children", ChildViewSet, basename="child")
# router.register(r"history", PictogramUsageView, basename="history")
# router.register(r"recomendation", RecomendationView, basename="recomendation")

usage_router = NestedSimpleRouter(router, r"children", lookup="child")
usage_router.register(r"picto-usage", UsageChildView, basename="child-usage")
collection_router = NestedSimpleRouter(router, r"children", lookup="child")
collection_router.register(r"collections", CollectionChildView, basename="child-collection")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(usage_router.urls)),
    path("", include(collection_router.urls)),
]

