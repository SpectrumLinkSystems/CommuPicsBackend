from .models import Therapist
from apps.child.models import Child
import cv2
from django.db.models import ObjectDoesNotExist

def create_therapist(data):
    allowed_fields = ['name', 'last_name', 'document_type', 'document_number',
                    'date_of_birth', 'document_front_validator', 
                    'document_back_validator', 'firebase_id']
    filtered_data = {key: value for key, value in data.items() if key in allowed_fields}
    therapist = Therapist.objects.create(**filtered_data)
    return therapist

def get_all_therapists():
    return Therapist.objects.all()

def assign_child_to_therapist(therapist_id, child_id):
    try:
        therapist = Therapist.objects.get(id=therapist_id)
        child = Child.objects.get(id=child_id)
        child.therapist = therapist
        child.save()
        return True
    except (Therapist.DoesNotExist, Child.DoesNotExist):
        return False

def unassign_child_from_therapist(therapist_id, child_id):
    try:
        child = Child.objects.get(id=child_id, therapists_id=therapist_id)
        child.therapists_id = None
        child.save()
        return True
    except Child.DoesNotExist:
        return False
    
def get_therapist_by_id(therapist_id):
    try:
        return Therapist.objects.get(id=therapist_id)
    except Therapist.DoesNotExist:
        return None

def update_therapist(therapist_id, data):
    try:
        therapist = Therapist.objects.get(id=therapist_id)
        allowed_fields = ['name', 'last_name', 'document_type', 'document_number',
                        'date_of_birth', 'document_front_validator', 
                        'document_back_validator']
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
    
def get_therapist_by_firebase_id(firebase_id):
    try:
        return Therapist.objects.get(firebase_id=firebase_id)
    except ObjectDoesNotExist:
        return None

def escanear_qr():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            cap.release()
            cv2.destroyAllWindows()
            return {"id_nino": data}

    cap.release()
    cv2.destroyAllWindows()
    return {"error": "No se detectó ningún QR"}
