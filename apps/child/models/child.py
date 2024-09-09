from django.db import models

class Child(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    autism_level = models.IntegerField()
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    parent = models.ForeignKey('parents.Parent', on_delete=models.CASCADE, related_name='children')
    therapists = models.ManyToManyField('therapists.Therapist', related_name='children_assigned')