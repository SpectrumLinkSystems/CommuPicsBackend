from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiParameter, extend_schema

from apps.external_apis.image_recognotion_service import ImageRecognitionService
from apps.images_storage.cloudinary_service import CloudinaryService
from apps.recognition.serializers import RecognitionRequestSerializer
from apps.child.models import Collection


class RecognitionView(APIView):
    def __init__(self):
        self.cloudinary_service = CloudinaryService()
        self.image_recognition_service = ImageRecognitionService()

    @extend_schema(
            request= RecognitionRequestSerializer,
            responses={200: "Recognition successfully"}
    )
    @action(
        detail=False, methods=["post"], url_path="recognize"
    )
    async def post(self, request):
        serializer = RecognitionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        child_id = serializer.validated_data["child_id"]
        image_url = serializer.validated_data["image_url"]

        collections = await sync_to_async(lambda: list(Collection.objects.filter(child_id=child_id).values()))()
        recognition_response = await self.image_recognition_service.recognize_image(image_url, collections)
        return Response(recognition_response, status=status.HTTP_200_OK)
