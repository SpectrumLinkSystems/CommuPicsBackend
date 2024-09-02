from rest_framework import viewsets
from profiles.serializers import ProfileTherapistSerializer
from profiles.models import ProfileTherapist

class ProfileTherapistViewSet(viewsets.ModelViewSet):
    queryset = ProfileTherapist.objects.all()
    serializer_class = ProfileTherapistSerializer