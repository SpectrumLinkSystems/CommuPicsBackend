from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response

from apps.child.serializers.collection_serializer import CollectionSerializer
from apps.external_apis.image_recognotion_service import ImageRecognitionService
from apps.images_storage.cloudinary_service import CloudinaryService
from apps.recognition.serializers import RecognotionSerializer
from apps.child.services.child_service import  get_child_collections

class RecognitionView(APIView):
    def __init__(self):
        self.cloudinary_service = CloudinaryService()
        self.image_recognition_service = ImageRecognitionService()

    def post(self, request):
        serializer = RecognotionSerializer(data=request.data)
        collections = get_child_collections(1)
        collection_serializer = CollectionSerializer(collections, many=True)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # recognition_response = await self.image_recognition_service.recognize_image(request.data["image"])
        # recognition_response["url_image"] = request.data["image"]
        recognition_response = self.image_recognition_service.recognize_image("https://unycos.com/cdn/shop/articles/La_importancia_de_la_relajacion_para_tocar_la_guitarra_1.jpg?v=1717643502", collections)
        return Response(recognition_response
                        , status=status.HTTP_201_CREATED)