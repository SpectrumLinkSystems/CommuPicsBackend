from django.db import models
from django.contrib.auth.models import User

class ProfileChild(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    date_of_birth = models.DateField() 
    autism_level = models.IntegerField(
        choices=[
            (1, 'Level 1 - Requiring Support'),
            (2, 'Level 2 - Requiring Substantial Support'),
            (3, 'Level 3 - Requiring Very Substantial Support')
        ],
        default=1
    )

    def __str__(self):
        return f"{self.name} - Autism Level {self.autism_level} - Child"