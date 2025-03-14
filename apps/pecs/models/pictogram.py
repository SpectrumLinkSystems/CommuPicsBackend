from django.conf.locale import da
from django.db import models

from apps.pecs.models.collection import Collection
from apps.child.models.child import Child


class Pictogram(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=255)
    arasaac_id = models.CharField(max_length=50)
    arasaac_categories = models.CharField(max_length=255)
    collection_id = models.ForeignKey(Collection, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "child_pictogram"


class PictogramUsage(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True)
    pictogram = models.ForeignKey(Pictogram, on_delete=models.CASCADE)
    date_used = models.DateTimeField(auto_now=True)
    cant_used = models.IntegerField(default=1)
    
    class Meta:
        db_table = "child_pictogramusage"
        unique_together = ['child', 'pictogram']

    def __str__(self):
        return f"{self.child.name} - {self.pictogram.name} - {self.date_used}"
