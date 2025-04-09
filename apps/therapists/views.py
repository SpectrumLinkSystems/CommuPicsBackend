from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.child.models.child import Child
from apps.child.models.pictogram import PictogramUsage
from apps.child.serializers.child_serializer import ChildSerializer
from apps.child.serializers.pictogram_usage_serializer import PictogramUsageSerializer

from .models import Therapist
from .serializers import TherapistSerializer
from .services import (create_therapist, get_all_therapists, get_therapist_by_id, update_therapist, delete_therapist, get_therapist_by_firebase_id, unassign_child_from_therapist)

class TherapistViewSet(viewsets.ModelViewSet):
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer

    def create(self, request, *args, **kwargs):
        therapist = create_therapist(request.data)
        serializer = TherapistSerializer(therapist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        therapists = get_all_therapists()
        serializer = TherapistSerializer(therapists, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='assign-child')
    def assign_child(self, request, pk=None):
        therapist = self.get_object()
        child_id = request.data.get('child_id')
        
        if not child_id:
            return Response(
                {"error": "El campo 'child_id' es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            child = Child.objects.get(id=child_id)
            
            if child.therapists_id == therapist:
                return Response(
                    {
                        "success": False,
                        "child_id": child.id,
                        "message": f"El niño {child.name} ya está asignado a este terapeuta"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            child.therapists_id = therapist
            child.save()
            
            return Response(
                {
                    "success": True,
                    "child_id": child.id,
                    "message": f"Niño {child.name} asignado correctamente"
                },
                status=status.HTTP_200_OK
            )
            
        except Child.DoesNotExist:
            return Response(
                {"error": f"No existe un niño con id {child_id}"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    @action(detail=True, methods=['post'], url_path='unassign-child')
    def unassign_child(self, request, pk=None):
        therapist_id = pk
        child_id = request.data.get('child_id')

        if not child_id:
            return Response(
                {"error": "El campo 'child_id' es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        success = unassign_child_from_therapist(therapist_id, child_id)

        if success:
            return Response(
                {"success": True, "message": f"Niño con id {child_id} desasignado correctamente"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"success": False, "message": f"No se pudo desasignar al niño con id {child_id} del terapeuta"},
            status=status.HTTP_400_BAD_REQUEST
        )


    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):

        therapist = get_object_or_404(Therapist, id=pk)
        children = therapist.children.all()
        
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        therapist_id = self.kwargs.get('pk')
        therapist = get_therapist_by_id(therapist_id)
        if therapist:
            serializer = TherapistSerializer(therapist)
            return Response(serializer.data)
        else:
            return Response({"error": "Therapist not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        therapist_id = self.kwargs.get('pk')
        therapist = update_therapist(therapist_id, request.data)
        if therapist:
            serializer = TherapistSerializer(therapist)
            return Response({"message": "Therapist updated", "therapist": serializer.data})
        else:
            return Response({"error": "Therapist not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        therapist_id = self.kwargs.get('pk')
        if delete_therapist(therapist_id):
            return Response({"message": "Therapist deleted"})
        else:
            return Response({"error": "Therapist not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def child_tracking(self, request, pk=None, child_id=None):
        therapist = get_object_or_404(Therapist, id=pk)
        child = get_object_or_404(Child, id=child_id)
        
        if child.therapist != therapist:
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
        return Response({"error": "Therapist not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        responses={200: {"type": "object", "properties": {"id_nino": {"type": "string"}}}},
    )
    @action(detail=False, methods=["get"])
    def escanear_qr_camara(self, request):

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not cap.isOpened():
            return Response({"error": "No se pudo acceder a la cámara"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

        return Response({"error": "No se detectó un código QR"}, status=status.HTTP_400_BAD_REQUEST)
