from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import request, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import qrcode
from io import BytesIO
import base64

from apps.child.models.child import Child
from apps.child.models.collection import Collection
from apps.child.serializers.child_serializer import ChildSerializer
from apps.child.serializers.collection_serializer import CollectionSerializer
from apps.child.services.child_service import create_child_for_parent, get_children_by_parent, get_child_by_parent, update_child_for_parent, delete_child_for_parent, update_autism_level, generar_qr;

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
        collections = Collection.objects.filter(child_id=child_id)
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        request=ChildSerializer,
        responses={200: ChildSerializer},
        parameters=[
            OpenApiParameter("child_id", OpenApiTypes.STR, OpenApiParameter.PATH),
            OpenApiParameter("autism_level", OpenApiTypes.INT, OpenApiParameter.QUERY),
        ],
    )
    @action(detail=True, methods=["patch"], url_path="update-autism-level")
    def update_autism_level_action(self, request, pk=None):
        child_id = pk
        parent_id = request.data.get("parent_id")
        new_autism_level = request.data.get("autism_level")

        if new_autism_level is None:
            return Response(
                {"error": "autism_level is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        child = update_autism_level(parent_id, child_id, new_autism_level)

        if not child:
            return Response(
                {"error": "Child not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChildSerializer(child)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="child_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="ID del niño para generar el QR"
            )
        ],
        responses={200: {"type": "object", "properties": {"qr_code": {"type": "string"}, "message": {"type": "string"}}}},
    )
    @action(detail=False, methods=["get"], url_path="generar-qr")
    def generar_qr_action(self, request):
        child_id = request.query_params.get("child_id")

        if not child_id:
            return Response(
                {"error": "El parámetro 'child_id' es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        qr_response = generar_qr(child_id)

        if "error" in qr_response:
            return Response(qr_response, status=status.HTTP_404_NOT_FOUND)

        return Response(qr_response, status=status.HTTP_200_OK)