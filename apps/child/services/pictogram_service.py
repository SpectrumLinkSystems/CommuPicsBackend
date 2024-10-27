from django.db.models import ObjectDoesNotExist

from apps.child.models import Pictogram
from apps.child.models.child import Child
from apps.child.models.collection import Collection
from apps.child.serializers.pictogram_serializer import \
    CreatePictogramSerializer


class PictogramService:
    def __init__(self):
        pass

    @staticmethod
    def create_pictogram(validated_data):
        name = validated_data["name"]
        image_url = validated_data["image_url"]
        collection_name = validated_data["collection_name"]
        child_id = validated_data["child_id"]

        try:
            child = Child.objects.get(id=child_id)
        except ObjectDoesNotExist:
            raise ValueError("Child does not exist")

        collection, created_collection = Collection.objects.get_or_create(
            name=collection_name, child=child, defaults={"image_url": image_url}
        )

        pictogram = Pictogram.objects.create(name=name, image_url=image_url)

        return pictogram
