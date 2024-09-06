from rest_framework import viewsets

from apps.child.models.child import Child
from apps.child.serializers.child_serializer import ChildSerializer

class ChildView(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
        