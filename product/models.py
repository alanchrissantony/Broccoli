from django.db import models
from cloudinary.models import CloudinaryField
from category.models import Category
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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


PRODUCT_CACHE_KEYS = [
    'products_{id}',
    'product_{id}',
    'related_products_{id}',
    'top_rated'
]

CATEGORY_CACHE_KEY = 'categories'

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache_key_list = [key.format(id=instance.id) for key in PRODUCT_CACHE_KEYS]

    for key in cache_key_list:
        cache.delete(key)

    cache.delete(CATEGORY_CACHE_KEY)

@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
    cache.delete(CATEGORY_CACHE_KEY)