from rest_framework import viewsets

from apps.child.models.collection import Collection, SubCollection
from apps.child.serializers.collection_serializer import CollectionSerializer, SubCollectionSerializer


class CollectionView(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class SubCollectionView(viewsets.ModelViewSet):
    queryset = SubCollection.objects.all()
    serializer_class = SubCollectionSerializer