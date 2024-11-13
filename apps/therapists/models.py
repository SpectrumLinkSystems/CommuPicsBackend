from django.db import models

class Therapist(models.Model):
    objects = models.Manager()
    DOCUMENT_TYPE_CHOICES = [
        ('DNI', 'DNI'),
        ('PASSPORT', 'Passport'),
    ]

    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPE_CHOICES)
    document_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    document_front_validator = models.BooleanField(default=False)
    document_back_validator = models.BooleanField(default=False)
    firebase_id = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name} {self.last_name}'
