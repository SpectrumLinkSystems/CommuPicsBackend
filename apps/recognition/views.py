from django.shortcuts import render
from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response

from apps import recognition
from apps.external_apis.image_recognotion_service import ImageRecognitionService
from apps.images_storage.cloudinary_service import CloudinaryService

class RecognitionView(APIView):
    def __init__(self):
        self.cloudinary_service = CloudinaryService()
        self.image_recognition_service = ImageRecognitionService()

    async def post(self, request):
        image_response = self.cloudinary_service.upload_image(image="/home/DRN-00X/Downloads/ice.jpg")
        image_url = image_response['url']
        recognition_response = await self.image_recognition_service.recognize_image(image_url)
        recognition_response["url_image"] = image_url
        return Response(recognition_response, status=status.HTTP_201_CREATED)