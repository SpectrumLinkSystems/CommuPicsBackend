from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import create_parent, get_all_parents, get_parent_by_id, update_parent, delete_parent

@api_view(['POST'])
def create_parent_view(request):
    parent = create_parent(request.data)
    return Response({"message": "Parent created", "parent": parent.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_all_parents_view(request):
    parents = get_all_parents()
    serialized_data = [{"id": p.id, "name": p.name, "last_name": p.last_name} for p in parents]
    return Response(serialized_data)

@api_view(['GET'])
def get_parent_view(request, parent_id):
    parent = get_parent_by_id(parent_id)
    if parent:
        return Response({"id": parent.id, "name": parent.name, "last_name": parent.last_name})
    else:
        return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_parent_view(request, parent_id):
    parent = update_parent(parent_id, request.data)
    if parent:
        return Response({"message": "Parent updated"})
    else:
        return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_parent_view(request, parent_id):
    if delete_parent(parent_id):
        return Response({"message": "Parent deleted"})
    else:
        return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)