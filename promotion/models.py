from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from product.models import Product
from category.models import Category

# Create your models here.
class Discount(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    discount = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class Coupon(models.Model):
    code = models.CharField(max_length=25, unique=True)
    minimum_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    maximum_redeem = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Promotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

class PromotionCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name