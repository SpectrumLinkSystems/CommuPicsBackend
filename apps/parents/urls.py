from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from apps.child.views.child_view import ChildViewSet

from .views import ParentViewSet

router = DefaultRouter()
router.register(r"parents", ParentViewSet, basename="parents")

#parents_router = NestedDefaultRouter(router, r"parents", lookup="parent")
#parents_router.register(r"children", ChildViewSet, basename="parent-children")

urlpatterns = [
    path("", include(router.urls)),
    #path("", include(parents_router.urls)),
]
