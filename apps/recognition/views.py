from adrf.views import APIView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from apps.child.services import child_service
from apps.external_apis.image_recognotion_service import ImageRecognitionService
from apps.images_storage.cloudinary_service import CloudinaryService
from apps.recognition.serializers import RecognotionSerializer

class RecognitionView(APIView):
    def __init__(self):
        self.cloudinary_service = CloudinaryService()
        self.image_recognition_service = ImageRecognitionService()

    @extend_schema(
            parameters=[
                OpenApiParameter("child_id", OpenApiTypes.STR, OpenApiParameter.PATH)
            ]
    )
    @action(
        detail=False, methods=["post"], url_path="recognize"
    )
    async def post(self, request):
        # collections = child_service.get_collections_by_child_id(request.user.child.id)
        collections = child_service.get_collections_by_child_id(1)
        # serializer = RecognotionSerializer("")
        # serializer = RecognotionSerializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        recognition_response = await self.image_recognition_service.recognize_image("", collections)
        # recognition_response = await self.image_recognition_service.recognize_image(request.data["image"], collections)
        return Response(recognition_response, status=status.HTTP_200_OK)
        # recognition_response["url_image"] = request.data["image"]
        # return Response(recognition_response, status=status.HTTP_201_CREATED)