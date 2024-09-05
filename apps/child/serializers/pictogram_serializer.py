from adrf import serializers

from apps.child.models.pictogram import Pictogram


class PictogramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictogram
        fields = '__all__'