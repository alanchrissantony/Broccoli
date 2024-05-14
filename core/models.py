from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image
from io import BytesIO
from uuid import uuid4
import os


# Create your models here.

def image_upload_path(instance, filename, folder):
    ext = filename.split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join(folder, filename)

