from rest_framework import serializers
from profiles.models import ProfileChild

class ProfileChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileChild
        fields = ['user', 'id', 'name', 'age', 'date_of_birth', 'autism_level']