from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import create_therapist, get_all_therapists, get_therapist_by_id, update_therapist, delete_therapist

@api_view(['POST'])
def create_therapist_view(request):
    therapist = create_therapist(request.data)
    return Response({"message": "Therapist created", "therapist": therapist.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_all_therapists_view(request):
    therapists = get_all_therapists()
    serialized_data = [{"id": t.id, "name": t.name, "last_name": t.last_name} for t in therapists]
    return Response(serialized_data)

@api_view(['GET'])
def get_therapist_view(request, therapist_id):
    therapist = get_therapist_by_id(therapist_id)
    if therapist:
        return Response({"id": therapist.id, "name": therapist.name, "last_name": therapist.last_name})
    else:
        return Response({"error": "Therapist not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_therapist_view(request, therapist_id):
    therapist = update_therapist(therapist_id, request.data)
    if therapist:
        return Response({"message": "Therapist updated"})
    else:
        return Response({"error": "Therapist not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_therapist_view(request, therapist_id):
    if delete_therapist(therapist_id):
        return Response({"message": "Therapist deleted"})
    else:
        return Response({"error": "Therapist not found"}, status=status.HTTP_404_NOT_FOUND)