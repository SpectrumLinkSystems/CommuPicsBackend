from django.db import models
from django.contrib.auth.models import User

class ProfileTherapist(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('DNI', 'DNI'),
        ('Passport', 'Passport'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    date_of_birth = models.DateField()
    document_number = models.CharField(max_length=100)
    front_document_image = models.ImageField(upload_to='documents/front/', blank=True, null=True)
    back_document_image = models.ImageField(upload_to='documents/back/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.document_number} - Therapist"