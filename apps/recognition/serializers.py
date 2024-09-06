from rest_framework import serializers

class RecognotionSerializer(serializers.Serializer):
    image = serializers.ImageField()
    class Meta:
        fields = '__all__'