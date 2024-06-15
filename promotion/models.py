from django.db import models
from product.models import Product
from category.models import Category
from datetime import date


# Create your models here.
class Discount(models.Model):

    TYPE = (
        ('Percentage Discount', 'Percentage Discount'),
        ('Payment Discount', 'Payment Discount')
    )
    
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50, choices=TYPE)
    discount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def is_active(self):
        today = date.today()
        return self.start_date <= today <= self.end_date

    @classmethod
    def auto_delete_expired(cls):
        today = date.today()
        expired_discounts = cls.objects.filter(end_date__lt=today)
        expired_discounts.delete()


class Coupon(models.Model):

    TYPE = (
        ('Percentage Discount', 'Percentage Discount'),
        ('Payment Discount', 'Payment Discount')
    )
    
    code = models.CharField(max_length=25, unique=True)
    type = models.CharField(max_length=50, choices=TYPE)
    minimum_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.FloatField()
    maximum_redeem = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    status = models.BooleanField(default=True)


    def __str__(self):
        return self.code
    
    
    def is_active(self):
        today = date.today()
        return self.expiry >= today and self.status  # Check both expiry and active status

    @classmethod
    def auto_delete_expired(cls):
        today = date.today()
        expired_coupons = cls.objects.filter(expiry__lt=today)
        expired_coupons.delete()


class Promotion(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name

class PromotionCategory(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Promotion Category'
        verbose_name_plural = 'Promotion Categories'

    def __str__(self):
        return self.category.name