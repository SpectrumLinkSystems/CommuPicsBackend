from rest_framework import serializers

from apps.child.models.pictogram import Pictogram


class PictogramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictogram
        fields = "__all__"


class CreatePictogramSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255)
    collection_name = serializers.CharField(max_length=255)
    child_id = serializers.IntegerField()

class CreateManyPictogramsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255)
    arasaac_id = serializers.CharField(max_length=50)
    arasaac_categories = serializers.CharField(max_length=255)
    collection_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)

