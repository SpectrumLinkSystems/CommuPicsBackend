from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Therapist
from .serializers import TherapistSerializer
from .services import create_therapist, get_all_therapists, get_therapist_by_id, update_therapist, delete_therapist

class TherapistViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        therapist = create_therapist(request.data)
        serializer = TherapistSerializer(therapist)
        return Response({"message": "Therapist created", "therapist": serializer.data}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        therapists = get_all_therapists()
        serializer = TherapistSerializer(therapists, many=True)
        return Response(serializer.data)

    def assign_child(self, request, *args, **kwargs):
        therapist_id = self.kwargs.get('pk')
        child_id = request.data.get('child_id')

        therapist = get_object_or_404(Therapist, id=therapist_id)
        child = get_object_or_404(Child, id=child_id)

        child.therapists.add(therapist)
        
        return Response({"message": f"Child {child.name} assigned to therapist {therapist.name}"}, status=status.HTTP_200_OK)

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
    
    def child_tracking(self, request, *args, **kwargs):
        therapist_id = self.kwargs.get('pk')
        child_id = request.data.get('child_id')

        therapist = get_object_or_404(Therapist, id=therapist_id)
        child = get_object_or_404(Child, id=child_id)
        if therapist not in child.therapists.all():
            raise PermissionDenied("You do not have access to this child's data.")

        pictogram_usages = PictogramUsage.objects.filter(child=child)
        serializer = PictogramUsageSerializer(pictogram_usages, many=True)
        return Response(serializer.data)