from adrf import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.child.models.pictogram import Pictogram
from apps.child.serializers.pictogram_serializer import (
    CreatePictogramSerializer, PictogramSerializer, CreateManyPictogramsSerializer)
from apps.child.services.pictogram_service import PictogramService, create_many_pictograms


class PictogramView(viewsets.ModelViewSet):
    queryset = Pictogram.objects.all()
    serializer_class = PictogramSerializer
    pictogram_service = PictogramService()

    @action(detail=False, methods=["post"])
    def create_pictogram(self, request):
        serializer = CreatePictogramSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pictogram = self.pictogram_service.create_pictogram(
                    serializer.validated_data
                )
                return Response(
                    PictogramSerializer(pictogram).data, status=status.HTTP_201_CREATED
                )
            except ValueError as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={201},
        request=CreateManyPictogramsSerializer
    )
    @action(detail=False, methods=["post"])
    def create_many_pictogram(self, request):
        serializer = CreateManyPictogramsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                create_many_pictograms(serializer)
                return Response(status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
