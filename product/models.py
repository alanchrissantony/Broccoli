from django.db import models
from cloudinary.models import CloudinaryField
from category.models import Category

# Create your models here.

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField('Image')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = CloudinaryField('image', blank=True)

    def __str__(self):
        return f"Image {self.id}"

