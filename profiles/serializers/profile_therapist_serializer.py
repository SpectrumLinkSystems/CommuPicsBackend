from rest_framework import serializers
from profiles.models import ProfileTherapist

class ProfileTherapistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileTherapist
        fields = ['user', 'id', 'name', 'document_type', 'date_of_birth', 'document_number', 'front_document_image', 'back_document_image']