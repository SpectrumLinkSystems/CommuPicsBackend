from rest_framework import serializers

from apps.child.models.child import Child

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'
        extra_kwargs = {
            'therapists_id': {'read_only': True}  # Para que no se asigne al crear
        }