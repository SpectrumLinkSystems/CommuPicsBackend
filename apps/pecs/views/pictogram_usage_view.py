from adrf import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.pecs.models.pictogram import PictogramUsage
from apps.pecs.serializers.pictogram_usage_serializer import PictogramUsageSerializer
from apps.pecs.services.pictogram_service import PictogramService

class PictogramUsageView(viewsets.ModelViewSet):
    queryset = PictogramUsage.objects.all()
    serializer_class = PictogramUsageSerializer
    pictogram_service = PictogramService()

    # @action(detail=False, methods=['post'])
    # def register_usage(self, request):
    #     pictogram_id = request.data.get('pictogram')
    #     child_id = request.data.get('child')

    #     if pictogram_id is None or child_id is None:
    #         return Response({"error": "Faltan 'pictogram' o 'child' en los datos."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # Usar el servicio para registrar el uso del pictograma
    #         usage = self.pictogram_service.register_pictogram_usage(pictogram_id, child_id)
    #         serializer = self.get_serializer(usage)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except ValueError as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UsageChildView(GenericViewSet, RetrieveModelMixin, CreateModelMixin):
    queryset = PictogramUsage.objects.all()
    serializer_class = PictogramUsageSerializer

    @action(detail=False, methods=['get'], url_path='history') # child/(?P<child_id>[^/.]+)
    def history_by_child(self, request, child_pk=None):
        pictogram_usage = PictogramUsage.objects.filter(child_id=child_pk)
        
        if not pictogram_usage.exists():
            return Response(
                {"detail": "No se encontró historial de uso para el niño especificado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serializar y devolver los datos
        serializer = self.get_serializer(pictogram_usage, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'], url_path='recommendations/(?P<pictogram_id>[^/.]+)')
    def recommendations_for_pictogram(self, request, child_pk=None, pictogram_id=None):
        if not pictogram_id:
            return Response(
                {"detail": "El ID del pictograma seleccionado es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        recommendations = get_pictogram_recommendations(child_pk, pictogram_id)

        if "error" in recommendations:
            return Response(
                {"detail": recommendations["error"]},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(recommendations, status=status.HTTP_200_OK)