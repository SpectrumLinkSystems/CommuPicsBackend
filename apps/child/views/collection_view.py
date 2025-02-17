from typing import List

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse, OpenApiRequest
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.child.models.collection import Collection
from apps.child.models.pictogram import Pictogram
from apps.child.serializers.collection_serializer import CollectionSerializer
from apps.child.serializers.pictogram_serializer import PictogramSerializer
from apps.child.services.collection_service import CollectionService


class CollectionView(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    @extend_schema(
        request=OpenApiRequest(
            request=CollectionSerializer(many=True),
        ),
        responses={201: OpenApiResponse(
            response=List[int]
        )},
    )
    @action(
        detail=False, methods=["post"], url_path="many"
    )
    def create_collections(self, request, *args, **kwargs):
        try:
            new_ids = CollectionService.create_many_collections(self, collections=request.data)
            return Response({'ids': new_ids}, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        try:
            collection = Collection.objects.get(id=collection_id)
            child = collection.child_id

            pictograms = Pictogram.objects.filter(collection_id=collection)

            # # Aplicar filtro según el nivel de autismo
            # if child.autism_level == 1:
            #     pictograms = pictograms.filter(arasaac_categories__icontains="core vocabulary")

            serializer = PictogramSerializer(pictograms, many=True)
            return Response(serializer.data)

        except Collection.DoesNotExist:
            return Response({"error": "Collection not found"}, status=404)