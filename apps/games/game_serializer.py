from rest_framework import serializers
from apps.child.models import Collection, Pictogram

class ClassificationCheckSerializer(serializers.Serializer):
    pictogram_id = serializers.IntegerField(min_value=1)
    collection_id = serializers.IntegerField(min_value=1)

    def validate(self, data):
        return data

class ClassificationResultSerializer(serializers.Serializer):
    is_correct = serializers.BooleanField()
    correct_collection_id = serializers.IntegerField()
    correct_collection_name = serializers.CharField()
    pictogram_id = serializers.IntegerField()
    selected_collection_id = serializers.IntegerField()

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'image_url']
        read_only_fields = fields

class PictogramSerializer(serializers.ModelSerializer):
    collection_name = serializers.CharField(source='collection.name', read_only=True)
    collection_image = serializers.CharField(source='collection.image_url', read_only=True)
    
    class Meta:
        model = Pictogram
        fields = [
            'id', 
            'name', 
            'image_url',
            'arasaac_id',
            'arasaac_categories',
            'collection_id',
            'collection_name',
            'collection_image'
        ]
        read_only_fields = fields