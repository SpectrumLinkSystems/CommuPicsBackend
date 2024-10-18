from django.db import models

class Pictogram(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=255)
    arasaac_id = models.CharField(max_length=50)
    arasaac_categories=models.CharField(max_length=255)
    subcollection = models.ForeignKey("SubCollection", on_delete=models.CASCADE)

class PictogramUsage(models.Model):
    pictogram = models.ForeignKey('Pictogram', on_delete=models.CASCADE)
    date_used = models.DateTimeField()
    cant_used = models.IntegerField(default=0) 

    def __str__(self):
        return f'{self.child.name} - {self.pictogram.name} - {self.date_used}'
