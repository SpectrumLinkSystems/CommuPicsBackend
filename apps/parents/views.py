from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.parents.models import Parent

from .serializers import ParentSerializer
from .services import (create_parent, delete_parent, get_all_parents,
                       get_parent_by_firebase_id, get_parent_by_id,
                       update_parent)

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    def create(self, request, *args, **kwargs):
        parent = create_parent(request.data)
        if parent:
            serializer = self.get_serializer(parent)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Failed to create parent"}, status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, *args, **kwargs):
        parents = get_all_parents()
        serializer = self.get_serializer(parents, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "firebase_id",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
            )
        ]
    )
    @action(detail=False, methods=["get"])
    def get_parent_by_firebase_id(self, request):
        firebase_id = request.query_params.get("firebase_id", None)
        print(firebase_id)
        if not firebase_id:
            return Response(
                {"error": "firebase_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        parent = get_parent_by_firebase_id(firebase_id)
        if parent:
            serializer = self.get_serializer(parent)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        parent_id = self.kwargs.get("pk")
        parent = get_parent_by_id(parent_id)
        if parent:
            serializer = self.get_serializer(parent)
            return Response(serializer.data)
        return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        parent_id = self.kwargs.get("pk")
        parent = update_parent(parent_id, request.data)
        if parent:
            serializer = self.get_serializer(parent)
            return Response({"message": "Parent updated", "parent": serializer.data})
        return Response(
            {"error": "Parent not found or failed to update"},
            status=status.HTTP_404_NOT_FOUND,
        )

    def destroy(self, request, *args, **kwargs):
        parent_id = self.kwargs.get("pk")
        if delete_parent(parent_id):
            return Response(
                {"message": "Parent deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)
