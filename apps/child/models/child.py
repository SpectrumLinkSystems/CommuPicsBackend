from django.db import models

class Child(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    autism_level = models.IntegerField()
    # parent = models.ForeignKey('parent.Parent', on_delete=models.CASCADE)