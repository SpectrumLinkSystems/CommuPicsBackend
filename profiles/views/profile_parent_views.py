from rest_framework import viewsets
from profiles.serializers import ProfileParentSerializer
from profiles.models import ProfileParent

class ProfileParentViewSet(viewsets.ModelViewSet):
    queryset = ProfileParent.objects.all()
    serializer_class = ProfileParentSerializer