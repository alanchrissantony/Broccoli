from django.db import models
from functools import partial
from core.models import image_upload_path 
import uuid

# Create your models here.
class Banner(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=partial(image_upload_path, folder='products'), blank=True)