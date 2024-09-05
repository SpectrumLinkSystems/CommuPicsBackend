from django.conf.locale import ro
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.child.views import ChildView, CollectionView, SubCollectionView, PictogramView

router =DefaultRouter()

router.register(r'children', ChildView, basename='child')
router.register(r'collections', CollectionView, basename='collection')
router.register(r'subcollections', SubCollectionView, basename='subcollection')
router.register(r'pictograms', PictogramView, basename='pictogram')

urlpatterns = [
    path('', include(router.urls)),
]
