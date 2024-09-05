from django.db import models

class Pictogram(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=255)
    subcollection = models.ForeignKey("SubCollection", on_delete=models.CASCADE)