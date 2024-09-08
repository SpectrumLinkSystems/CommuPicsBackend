from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response

from apps.external_apis.image_recognotion_service import ImageRecognitionService
from apps.images_storage.cloudinary_service import CloudinaryService
from apps.recognition.serializers import RecognotionSerializer

class RecognitionView(APIView):
    def __init__(self):
        self.cloudinary_service = CloudinaryService()
        self.image_recognition_service = ImageRecognitionService()

    async def post(self, request):
        serializer = RecognotionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        recognition_response = await self.image_recognition_service.recognize_image(request.data["image"])
        recognition_response["url_image"] = request.data["image"]
        return Response(recognition_response, status=status.HTTP_201_CREATED)