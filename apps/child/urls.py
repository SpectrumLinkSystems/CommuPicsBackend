from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from apps.child.views.child_view import ChildViewSet
from apps.child.views.collection_view import CollectionView
from apps.child.views.generate_sentences import SentenceGameViewSet
from apps.child.views.pictogram_view import PictogramView
from apps.child.views.pictogram_usage_view import PictogramUsageView
from apps.games.classification.clasification_view import ClassificationGameViewSet
from apps.games.recomendation.recomendation_view import RecomendationView


router = DefaultRouter()
router.register(r"children", ChildViewSet, basename="child")
router.register(r"collections", CollectionView, basename="collection")
router.register(r"pictograms", PictogramView, basename="pictogram")
router.register(r"history", PictogramUsageView, basename="history")
router.register(r"recomendation", RecomendationView, basename="recomendation")
router.register(r"clasification", ClassificationGameViewSet, basename="clasification")
router.register(r"game", SentenceGameViewSet, basename="game")

urlpatterns = [
    path("", include(router.urls)),
]

