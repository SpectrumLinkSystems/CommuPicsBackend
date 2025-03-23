from rest_framework import serializers

class SentenceGamePictogramSerializer(serializers.Serializer):
    name = serializers.CharField()
    image_url = serializers.CharField()
    arasaac_id = serializers.CharField()
    arasaac_categories = serializers.CharField()
    collection_id = serializers.IntegerField()