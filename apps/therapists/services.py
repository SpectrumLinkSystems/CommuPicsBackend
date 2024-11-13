from .models import Therapist
from apps.child.models import Child

from django.db.models import ObjectDoesNotExist

def create_therapist(data):
    allowed_fields = ['name', 'last_name', 'document_type', 'document_number','date_of_birth', 'document_front_validator', 'document_back_validator']
    filtered_data = {key: value for key, value in data.items() if key in allowed_fields}
    therapist = Therapist.objects.create(**filtered_data)
    return therapist

def get_all_therapists():
    return Therapist.objects.all()

def assign_child_to_therapist(therapist_id, child_id):
    try:
        therapist = Therapist.objects.get(id=therapist_id)
        child = Child.objects.get(id=child_id)
        child.therapists.add(therapist)
        return True
    except (Therapist.DoesNotExist, Child.DoesNotExist):
        return False

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

def child_tracking(request, child_id):
    child = Child.objects.get(id=child_id)
    
    if request.user.is_parent and child.parent != request.user.parent:
        raise PermissionDenied
    if request.user.is_therapist and not request.user.therapist.children.filter(id=child_id).exists():
        raise PermissionDenied

    pictogram_usages = child.pictogram_usages.all()

    return render(request, 'child_tracking.html', {'child': child, 'pictogram_usages': pictogram_usages})

def get_therapist_by_firebase_id(firebase_id):
    try:
        return Therapist.objects.get(firebase_id=firebase_id)
    except ObjectDoesNotExist:
        return None
