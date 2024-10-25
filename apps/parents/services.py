from django.db.models import ObjectDoesNotExist

from .models import Parent


def create_parent(data):
    allowed_fields = [
        "name",
        "last_name",
        "document_type",
        "document_number",
        "date_of_birth",
        "document_front_validator",
        "document_back_validator",
        "firebase_id",
    ]
    filtered_data = {key: value for key, value in data.items() if key in allowed_fields}
    parent = Parent.objects.create(**filtered_data)
    return parent


def get_all_parents():
    return Parent.objects.all()


def get_parent_by_id(parent_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        return parent
    except ObjectDoesNotExist:
        return None


def get_parent_by_firebase_id(firebase_id):
    try:
        return Parent.objects.get(firebase_id=firebase_id)
    except ObjectDoesNotExist:
        return None


def update_parent(parent_id, data):
    try:
        parent = Parent.objects.get(id=parent_id)
        allowed_fields = [
            "name",
            "last_name",
            "document_type",
            "document_number",
            "date_of_birth",
            "document_front_validator",
            "document_back_validator",
        ]
        for key, value in data.items():
            if key in allowed_fields:
                setattr(parent, key, value)
        parent.save()
        return parent
    except ObjectDoesNotExist:
        return None


def delete_parent(parent_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        parent.delete()
        return True
    except ObjectDoesNotExist:
        return False
