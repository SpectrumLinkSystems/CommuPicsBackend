from adrf import viewsets

from apps.child.models.pictogram import Pictogram
from apps.child.serializers.pictogram_serializer import PictogramSerializer


class PictogramView(viewsets.ModelViewSet):
    queryset = Pictogram.objects.all()
    serializer_class = PictogramSerializer