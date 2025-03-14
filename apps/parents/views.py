from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.parents.models import Parent

from .serializers import ParentSerializer
from .services import (
    get_parent_by_firebase_id,
)


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

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
