from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Parent
from .serializers import ParentSerializer
from .services import create_parent, get_all_parents, get_parent_by_id, update_parent, delete_parent

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    def create(self, request, *args, **kwargs):
        parent = create_parent(request.data)
        serializer = self.get_serializer(parent)
        return Response({"message": "Parent created", "parent": serializer.data}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        parents = get_all_parents()
        serializer = self.get_serializer(parents, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        parent_id = self.kwargs.get('pk')
        parent = get_parent_by_id(parent_id)
        if parent:
            serializer = self.get_serializer(parent)
            return Response(serializer.data)
        else:
            return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        parent_id = self.kwargs.get('pk')
        parent = update_parent(parent_id, request.data)
        if parent:
            serializer = self.get_serializer(parent)
            return Response({"message": "Parent updated", "parent": serializer.data})
        else:
            return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        parent_id = self.kwargs.get('pk')
        if delete_parent(parent_id):
            return Response({"message": "Parent deleted"})
        else:
            return Response({"error": "Parent not found"}, status=status.HTTP_404_NOT_FOUND)