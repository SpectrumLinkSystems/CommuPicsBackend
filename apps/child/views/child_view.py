from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import request, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.child.models.child import Child
from apps.child.models.collection import Collection
from apps.child.serializers.child_serializer import ChildSerializer
from apps.child.serializers.collection_serializer import CollectionSerializer
from apps.child.services.child_service import create_child_for_parent, get_children_by_parent, get_child_by_parent, update_child_for_parent, delete_child_for_parent;

class ChildViewSet(viewsets.ModelViewSet):
    serializer_class = ChildSerializer

    def get_queryset(self):
        parent_id = self.kwargs.get("parent_pk")
        if parent_id:
            return Child.objects.filter(parent_id=parent_id)
        return Child.objects.all()
    
    def create(self, request, *args, **kwargs):
        parent_id = request.data.get("parent_id")
        child_data = request.data

        if not parent_id:
            return Response({"error": "parent_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        child = create_child_for_parent(parent_id, child_data)

        if not child:
            return Response({"error": "Could not create child. Check server logs for more details."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ChildSerializer(child)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses={200: CollectionSerializer(many=True)},
        parameters=[
            OpenApiParameter("child_id", OpenApiTypes.STR, OpenApiParameter.PATH)
        ],
    )
    @action(detail=False, methods=["get"], url_path="(?P<child_id>[^/.]+)/collections")
    def get_collections_by_child_id(self, request, child_id):
        collections = Collection.objects.filter(child=child_id)
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
