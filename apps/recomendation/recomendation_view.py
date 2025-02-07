from adrf import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from apps.recomendation.recomendation_service import get_pictogram_recommendations
from apps.child.serializers.pictogram_serializer import (
    CreatePictogramSerializer, PictogramSerializer)
from apps.child.services.pictogram_service import PictogramService
from apps.child.models.pictogram import PictogramUsage
from apps.child.serializers.pictogram_usage_serializer import PictogramUsageSerializer
from apps.child.services.pictogram_service import PictogramService


class RecomendationView(viewsets.ModelViewSet):
    serializer_class = PictogramUsageSerializer

    @action(detail=False, methods=['get'], url_path='(?P<child_id>[^/.]+)/(?P<pictogram_id>[^/.]+)')
    def recommendations_for_pictogram(self, request, child_id=None, pictogram_id=None):
        if not pictogram_id:
            return Response(
                {"detail": "El ID del pictograma seleccionado es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        recommendations = get_pictogram_recommendations(child_id, pictogram_id)

        if "error" in recommendations:
            return Response(
                {"detail": recommendations["error"]},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(recommendations, status=status.HTTP_200_OK)