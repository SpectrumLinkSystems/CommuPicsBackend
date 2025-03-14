from django.db import models

from apps.child.models.child import Child


class Collection(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=255)
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE)

    class Meta:
        db_table = "child_collection"