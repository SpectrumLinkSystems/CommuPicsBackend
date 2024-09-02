from rest_framework import viewsets
from profiles.serializers import ProfileChildSerializer
from profiles.models import ProfileChild

class ProfileChildViewSet(viewsets.ModelViewSet):
    queryset = ProfileChild.objects.all()
    serializer_class = ProfileChildSerializer