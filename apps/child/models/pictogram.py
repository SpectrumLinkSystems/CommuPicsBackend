from django.db import models

from apps.child.models.collection import Collection


class Pictogram(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=255)
    arasaac_id = models.CharField(max_length=50)
    arasaac_categories = models.CharField(max_length=255)
    collection_id = models.ForeignKey(Collection, on_delete=models.CASCADE)


class PictogramUsage(models.Model):
    pictogra_id = models.ForeignKey(Pictogram, on_delete=models.CASCADE)
    date_used = models.DateTimeField()
    cant_used = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.child.name} - {self.pictogram.name} - {self.date_used}"
