from django.db.models import ObjectDoesNotExist
from django.db import transaction
from apps.child.models import Child
from apps.parents.models import Parent
from apps.child.models import Collection, Pictogram
from .default_collections import DEFAULT_COLLECTIONS


def create_child_for_parent(parent_id, child_data):
    try:
        parent = Parent.objects.get(id=parent_id)
        
        allowed_fields = [
            "name",
            "last_name",
            "birth_date",
            "autism_level",
            "avatar",
        ]
        
        filtered_data = {
            key: value for key, value in child_data.items() if key in allowed_fields
        }
        
        with transaction.atomic(): 

            child = Child.objects.create(parent_id=parent, **filtered_data)

            for collection_data in DEFAULT_COLLECTIONS:
                collection = Collection.objects.create(
                    name=collection_data["name"],
                    image_url=collection_data["image_url"],
                    child_id=child,
                )

                for pictogram_data in collection_data["pictograms"]:
                    Pictogram.objects.create(
                        name=pictogram_data["name"],
                        image_url=pictogram_data["image_url"],
                        arasaac_id=pictogram_data["arasaac_id"],
                        arasaac_categories=pictogram_data["arasaac_categories"],
                        collection_id=collection,
                    )
        return child

    except ObjectDoesNotExist:
        return None

def get_children_by_parent(parent_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        return Child.objects.filter(parent=parent)
    except ObjectDoesNotExist:
        return None


def get_child_by_parent(parent_id, child_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        return Child.objects.get(parent=parent, id=child_id)
    except (ObjectDoesNotExist, ObjectDoesNotExist):
        return None


def update_child_for_parent(parent_id, child_id, data):
    try:
        parent = Parent.objects.get(id=parent_id)
        child = Child.objects.get(parent=parent, id=child_id)
        allowed_fields = ["name", "last_name", "birth_date", "autism_level", "avatar"]
        for key, value in data.items():
            if key in allowed_fields:
                setattr(child, key, value)
        child.save()
        return child
    except (ObjectDoesNotExist, ObjectDoesNotExist):
        return None


def delete_child_for_parent(parent_id, child_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        child = Child.objects.get(parent=parent, id=child_id)
        child.delete()
        return True
    except (ObjectDoesNotExist, ObjectDoesNotExist):
        return False


def count_children(parent_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        return Child.objects.filter(parent=parent).count()
    except ObjectDoesNotExist:
        return 0

def update_autism_level(parent_id, child_id, new_autism_level):
    try:
        parent = Parent.objects.get(id=parent_id)
        child = Child.objects.get(parent_id=parent, id=child_id)

        child.autism_level = new_autism_level
        child.save()

        return child

    except ObjectDoesNotExist:
        return None
