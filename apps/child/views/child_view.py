from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from apps.child.models.child import Child
from apps.child.serializers.child_serializer import ChildSerializer
from apps.child.services.child_service import (create_child_for_parent, get_children_by_parent, get_children_by_parent, update_child_for_parent, delete_child_for_parent, count_children)
class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    def create(self, request, parent_pk=None):
        child = create_child_for_parent(parent_pk, request.data, request.FILES.get('avatar'))
        if child:
            serializer = ChildSerializer(child)
            return Response({"message": "Child created", "child": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": "Failed to create child or parent not found"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, parent_pk=None):
        children = get_children_by_parent(parent_pk)
        if children is not None:
            serializer = ChildSerializer(children, many=True)
            return Response(serializer.data)
        return Response({"error": "Parent not found or no children"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, parent_pk=None, pk=None):
        child = get_child_by_parent(parent_pk, pk)
        if child:
            serializer = ChildSerializer(child)
            return Response(serializer.data)
        return Response({"error": "Child or Parent not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, parent_pk=None, pk=None):
        # Handle file uploads if present
        child = update_child_for_parent(parent_pk, pk, request.data, request.FILES.get('avatar'))
        if child:
            serializer = ChildSerializer(child)
            return Response({"message": "Child updated", "child": serializer.data})
        return Response({"error": "Child or Parent not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, parent_pk=None, pk=None):
        if delete_child_for_parent(parent_pk, pk):
            return Response({"message": "Child deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Child or Parent not found"}, status=status.HTTP_404_NOT_FOUND)
    