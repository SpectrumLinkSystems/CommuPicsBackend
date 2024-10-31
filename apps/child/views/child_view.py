from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import request, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.child.models.child import Child
from apps.child.models.collection import Collection
from apps.child.serializers.child_serializer import ChildSerializer
from apps.child.serializers.collection_serializer import CollectionSerializer


class ChildViewSet(viewsets.ModelViewSet):
    serializer_class = ChildSerializer

    def get_queryset(self):
        parent_id = self.kwargs.get("parent_pk")
        if parent_id:
            return Child.objects.filter(parent_id=parent_id)
        return Child.objects.all()

    @extend_schema(
        responses={200: CollectionSerializer(many=True)},
        parameters=[
            OpenApiParameter("child_id", OpenApiTypes.STR, OpenApiParameter.PATH)
        ],
    )
    @action(detail=False, methods=["get"], url_path="(?P<child_id>[^/.]+)/collections")
    def get_collections_by_child_id(self, request, child_id):
        collections = Collection.objects.filter(child_id=child_id)
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
