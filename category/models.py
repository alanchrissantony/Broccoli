from django.db import models
from cloudinary.models import CloudinaryField



# Create your models here.

class Category(models.Model):
    
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    image = CloudinaryField('image', blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('name',)

    def __str__(self):
        return self.name
    

