from django.db import models
from functools import partial
from core.models import image_upload_path 

# Create your models here.
class Banner(models.Model):
    image = models.ImageField(upload_to=partial(image_upload_path, folder='products'), blank=True)