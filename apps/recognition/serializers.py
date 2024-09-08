from rest_framework import serializers

class RecognotionSerializer(serializers.Serializer):
    image = serializers.CharField(max_length=255)
    class Meta:
        fields = '__all__'