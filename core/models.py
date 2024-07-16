from django.db import models
from uuid import uuid4
import os


# Create your models here.

def image_upload_path(instance, filename, folder):
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join(folder, filename)


class Crop(models.Model):

    code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code