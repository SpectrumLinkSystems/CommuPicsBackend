from django.db import models

class Pictogram(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=255)
    subcollection = models.ForeignKey("SubCollection", on_delete=models.CASCADE)

class PictogramUsage(models.Model):
    child = models.ForeignKey('Child', on_delete=models.CASCADE, related_name='pictogram_usages')
    pictogram = models.ForeignKey('Pictogram', on_delete=models.CASCADE)
    date_used = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.child.name} - {self.pictogram.name} - {self.date_used}'