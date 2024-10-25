from django.db import models

from apps.parents.models import Parent
from apps.therapists.models import Therapist


class Child(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    autism_level = models.IntegerField()
    avatar = models.CharField(max_length=255)
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    therapists_id = models.ForeignKey(Therapist, null=True, on_delete=models.SET_NULL)
