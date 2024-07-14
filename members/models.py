# members/models.py
from django.db import models

class CropPrice(models.Model):
    crop_name = models.CharField(max_length=255)
    modal_price = models.FloatField()

    def __str__(self):
        return f"{self.crop_name} - {self.modal_price}"


# Create your models here.
