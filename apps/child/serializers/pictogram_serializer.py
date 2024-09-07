from rest_framework import serializers

from apps.child.models.pictogram import Pictogram

class PictogramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictogram
        fields = '__all__'

class CreatePictogramSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255)
    collection_name = serializers.CharField(max_length=255)
    subcollection_name = serializers.CharField(max_length=255)
    child_id = serializers.IntegerField()