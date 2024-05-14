from django.db import models
from functools import partial
from core.models import image_upload_path
from category.models import Category
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField('Image', related_name='products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    

class Image(models.Model):
    image = models.ImageField(upload_to=partial(image_upload_path, folder='products'), blank=True)

    def __str__(self):
        return f"Image {self.id}"