from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.child.models.collection import Collection
from apps.child.models.pictogram import Pictogram
from apps.child.serializers.collection_serializer import CollectionSerializer
from apps.child.serializers.pictogram_serializer import PictogramSerializer


class CollectionView(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    @extend_schema(
        responses={200: PictogramSerializer(many=True)},
        parameters=[
            OpenApiParameter("collection_id", OpenApiTypes.STR, OpenApiParameter.PATH)
        ],
    )
    @action(
        detail=False, methods=["get"], url_path="(?P<collection_id>[^/.]+)/pictograms"
    )
    def get_pictograms_by_collection_id(self, request, collection_id):
        collections = Pictogram.objects.filter(collection_id=collection_id)
        serializer = PictogramSerializer(collections, many=True)
        return Response(serializer.data)
