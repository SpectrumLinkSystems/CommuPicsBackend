from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action, api_view, parser_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import numpy as np

from .models import Therapist
from .serializers import TherapistSerializer
from .services import (
    get_therapist_by_firebase_id,
)


class TherapistViewSet(viewsets.ModelViewSet):
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer

    def assign_child(self, request, *args, **kwargs):
        therapist_id = self.kwargs.get("pk")
        child_id = request.data.get("child_id")

        therapist = get_object_or_404(Therapist, id=therapist_id)
        child = get_object_or_404(Child, id=child_id)

        child.therapists.add(therapist)

        return Response(
            {"message": f"Child {child.name} assigned to therapist {therapist.name}"},
            status=status.HTTP_200_OK,
        )

    def child_tracking(self, request, *args, **kwargs):
        therapist_id = self.kwargs.get("pk")
        child_id = request.data.get("child_id")

        therapist = get_object_or_404(Therapist, id=therapist_id)
        child = get_object_or_404(Child, id=child_id)
        if therapist not in child.therapists.all():
            raise PermissionDenied("You do not have access to this child's data.")

        pictogram_usages = PictogramUsage.objects.filter(child=child)
        serializer = PictogramUsageSerializer(pictogram_usages, many=True)
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
    def get_therapist_by_firebase_id(self, request):
        firebase_id = request.query_params.get("firebase_id", None)
        if not firebase_id:
            return Response(
                {"error": "firebase_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        therapist = get_therapist_by_firebase_id(firebase_id)
        if therapist:
            serializer = self.get_serializer(therapist)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Therapist not found"}, status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        responses={
            200: {"type": "object", "properties": {"id_nino": {"type": "string"}}}
        },
    )
    @action(detail=False, methods=["get"])
    def escanear_qr_camara(self, request):
        """Escanea un código QR en tiempo real usando la cámara."""
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Evita errores en Windows

        if not cap.isOpened():
            return Response(
                {"error": "No se pudo acceder a la cámara"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        detector = cv2.QRCodeDetector()

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                data, _, _ = detector.detectAndDecode(frame)
                if data:
                    return Response({"id_nino": data}, status=status.HTTP_200_OK)

                cv2.imshow("Escanear QR", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

        return Response(
            {"error": "No se detectó un código QR"}, status=status.HTTP_400_BAD_REQUEST
        )
