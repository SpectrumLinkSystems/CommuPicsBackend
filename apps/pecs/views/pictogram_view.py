from adrf import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.pecs.models.pictogram import Pictogram
from apps.pecs.serializers.pictogram_serializer import (
    CreatePictogramSerializer,
    PictogramSerializer,
    CreateManyPictogramsSerializer,
)
from apps.pecs.services.pictogram_service import (
    PictogramService,
    create_many_pictograms,
)


class PictogramView(viewsets.ModelViewSet):
    queryset = Pictogram.objects.all()
    serializer_class = PictogramSerializer
    pictogram_service = PictogramService()

    @extend_schema(responses={201}, request=CreateManyPictogramsSerializer)
    @action(detail=False, methods=["post"])
    def create_many_pictogram(self, request):
        serializer = CreateManyPictogramsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                create_many_pictograms(serializer)
                return Response(status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class PictogramCollectionView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Pictogram.objects.all()
    serializer_class = PictogramSerializer
    pictogram_service = PictogramService()
