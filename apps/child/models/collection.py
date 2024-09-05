from django.db import models

class Collection(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=255)
    child = models.ForeignKey('Child', on_delete=models.CASCADE)

class SubCollection(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=255)
    collection = models.OneToOneField('Collection', on_delete=models.CASCADE)