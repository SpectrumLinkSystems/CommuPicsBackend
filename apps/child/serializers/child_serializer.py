from rest_framework import serializers

from apps.child.models.child import Child

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'