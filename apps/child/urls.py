from django.conf.locale import ro
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.child.views.child_view import ChildView
from apps.child.views.collection_view import CollectionView
from apps.child.views.pictogram_view import PictogramView

router =DefaultRouter()

router.register(r'children', ChildView, basename='child')
router.register(r'collections', CollectionView, basename='collection')
router.register(r'subcollections', CollectionView, basename='subcollection')
router.register(r'pictograms', PictogramView, basename='pictogram')

urlpatterns = [
    path('', include(router.urls)),
]
