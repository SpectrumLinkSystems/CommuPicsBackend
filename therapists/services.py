from .models import Therapist

# Create Therapist
def create_therapist(data):
    therapist = Therapist.objects.create(**data)
    return therapist

# Read: Get all therapists
def get_all_therapists():
    return Therapist.objects.all()

# Read: Get therapist by ID
def get_therapist_by_id(therapist_id):
    try:
        return Therapist.objects.get(id=therapist_id)
    except Therapist.DoesNotExist:
        return None

# Update Therapist
def update_therapist(therapist_id, data):
    try:
        therapist = Therapist.objects.get(id=therapist_id)
        for key, value in data.items():
            setattr(therapist, key, value)
        therapist.save()
        return therapist
    except Therapist.DoesNotExist:
        return None

# Delete Therapist
def delete_therapist(therapist_id):
    try:
        therapist = Therapist.objects.get(id=therapist_id)
        therapist.delete()
        return True
    except Therapist.DoesNotExist:
        return False