from rest_framework import serializers


class RecognitionRequestSerializer(serializers.Serializer):
    child_id = serializers.IntegerField(required=True)
    image_url = serializers.CharField(required=True, max_length=255)
