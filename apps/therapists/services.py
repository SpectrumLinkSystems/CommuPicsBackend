# services.py
from .models import Therapist

def create_therapist(data):
    allowed_fields = ['name', 'last_name', 'document_type', 'document_number','date_of_birth', 'document_front_validator', 'document_back_validator']
    filtered_data = {key: value for key, value in data.items() if key in allowed_fields}
    therapist = Therapist.objects.create(**filtered_data)
    return therapist

def get_all_therapists():
    return Therapist.objects.all()


def get_therapist_by_id(therapist_id):
    try:
        return Therapist.objects.get(id=therapist_id)
    except Therapist.DoesNotExist:
        return None


def update_therapist(therapist_id, data):
    try:
        therapist = Therapist.objects.get(id=therapist_id)
        allowed_fields =  ['name', 'last_name', 'document_type', 'document_number','date_of_birth', 'document_front_validator', 'document_back_validator']
        for key, value in data.items():
            if key in allowed_fields:
                setattr(therapist, key, value)
        therapist.save()
        return therapist
    except Therapist.DoesNotExist:
        return None


def delete_therapist(therapist_id):
    try:
        therapist = Therapist.objects.get(id=therapist_id)
        therapist.delete()
        return True
    except Therapist.DoesNotExist:
        return False