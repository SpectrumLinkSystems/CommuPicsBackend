from django.db import transaction
from django.db.models import ObjectDoesNotExist
from django.utils import timezone

from apps.child.models import Pictogram
from apps.child.models.child import Child
from apps.child.models.collection import Collection
from apps.child.models.pictogram import PictogramUsage
from apps.child.serializers.pictogram_serializer import (
    CreateManyPictogramsSerializer,
)


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

    @staticmethod
    def register_pictogram_usage(pictogram_id, child_id):
        try:
            with transaction.atomic():
                # Verificar que existan el pictograma y el niño
                pictogram = Pictogram.objects.get(id=pictogram_id)
                child = Child.objects.get(id=child_id)

                # Intentar obtener o crear el registro
                usage, created = PictogramUsage.objects.get_or_create(
                    pictogram=pictogram,
                    child=child,
                    defaults={"cant_used": 1, "date_used": timezone.now()},
                )

                if not created:
                    # Si el registro ya existe, incrementar el contador
                    usage.cant_used += 1
                    usage.date_used = timezone.now()
                    usage.save()

                return usage

        except Child.DoesNotExist:
            raise ValueError("Child does not exist")
        except Pictogram.DoesNotExist:
            raise ValueError("Pictogram does not exist")
        except Exception as e:
            raise ValueError(f"Error registering pictogram usage: {str(e)}")


def create_many_pictograms(pictogram_data: CreateManyPictogramsSerializer):
    try:
        pictograms = []
        picto_name = pictogram_data["name"].value
        for collection_id in pictogram_data["collection_ids"].value:
            exists_pictogram = Pictogram.objects.get(
                name=picto_name.capitalize(), collection_id=collection_id
            )
            if not exists_pictogram:
                pictograms.append(
                    Pictogram(
                        name=pictogram_data["name"].value,
                        image_url=pictogram_data["image_url"].value,
                        arasaac_id=pictogram_data["arasaac_id"].value,
                        arasaac_categories=pictogram_data["arasaac_categories"].value,
                        collection_id=Collection(id=collection_id),
                    )
                )

        Pictogram.objects.bulk_create(pictograms)
    except ObjectDoesNotExist:
        raise ValueError("Collection does not exist")

    # json_data = await ArasaacService.search_pictograms_by_word(name)
    # pictogram_id = await ArasaacService.get_pictogram_id(json_data)
