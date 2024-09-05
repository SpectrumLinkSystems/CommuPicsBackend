from rest_framework import serializers

from apps.child.models.collection import Collection, SubCollection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class SubCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCollection
        fields = '__all__'