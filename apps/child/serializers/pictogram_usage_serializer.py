from rest_framework import serializers

from apps.child.models.pictogram import PictogramUsage

class PictogramUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictogramUsage
        fields = '__all__'
