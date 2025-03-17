from rest_framework import serializers
from apps.child.models.pictogram import Pictogram

class SentenceGamePictogramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictogram
        fields = "__all__"
        extra_kwargs = {
            'collection_id': {'source': 'collection_id_id'} 
        }