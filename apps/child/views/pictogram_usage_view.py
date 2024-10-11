from adrf import viewsets

from apps.child.models.pictogram import PictogramUsage
from apps.child.serializers.pictogram_usage_serializer import PictogramUsageSerializer

class PictogramUsageView(viewsets.ModelViewSet):
    queryset = PictogramUsage.objects.all()
    serializer_class = PictogramUsageSerializer