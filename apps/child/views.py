from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from adrf.views import APIView
from apps.external_apis.arasaac import ExternalApiArasaac
from apps.images_storage.azure_service import AzureService
from apps.external_apis.image_recognotion_service import ImageRecognitionService
from apps.images_storage.cloudinary_service import CloudinaryService

class ChildView(APIView):
    def __init__(self):
        self.cloudinary_service = CloudinaryService()

    async def get(self, request):
        # response = await ImageRecognitionService.recognize_image()
        # return Response(response, status=status.HTTP_200_OK)
        response = await ExternalApiArasaac.search_berry()
        return Response(response, status=status.HTTP_200_OK)
    
    async def post(self, request):
        # response = await ImageRecognitionService.recognize_image()
        # return Response(response, status=status.HTTP_201_CREATED)
        response = self.cloudinary_service.upload_image(image="/home/DRN-00X/Downloads/milk_photo.jpg")
        return Response(response, status=status.HTTP_201_CREATED)
