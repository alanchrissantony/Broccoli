from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.
class Banner(models.Model): 
    image = CloudinaryField('image', blank=True)

    def __str__(self):
        return f"Image {self.id}"

class Slide(models.Model):
    image = CloudinaryField('image', blank=True)

    def __str__(self):
        return f"Image {self.id}"