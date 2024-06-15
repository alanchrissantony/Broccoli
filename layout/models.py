from django.db import models
from functools import partial
from core.models import image_upload_path 


# Create your models here.
class Banner(models.Model): 
    image = models.ImageField(upload_to=partial(image_upload_path, folder='banner'), blank=True)

class Slide(models.Model):
    image = models.ImageField(upload_to=partial(image_upload_path, folder='slides'), blank=True)



    def __str__(self):
        return f"Image {self.id}"