from rest_framework import serializers
from profiles.models import ProfileParent

class ProfileParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileParent
        fields = ['user', 'id', 'name', 'document_type', 'date_of_birth', 'document_number', 'front_document_image', 'back_document_image']