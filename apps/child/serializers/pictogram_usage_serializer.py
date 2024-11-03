from rest_framework import serializers

from apps.child.models.pictogram import PictogramUsage
from apps.child.serializers.pictogram_serializer import PictogramSerializer

class PictogramUsageSerializer(serializers.ModelSerializer):
    pictogram_data = PictogramSerializer(source='pictogram', read_only=True)
    
    class Meta:
        model = PictogramUsage
        fields = ['child', 'pictogram', 'pictogram_data', 'date_used', 'cant_used']
        read_only_fields = ['date_used', 'cant_used', 'pictogram_data']