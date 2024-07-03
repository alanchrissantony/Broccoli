from django.db import models
from product.models import Product
from category.models import Category
from accounts.models import Account
from django.utils.timezone import now


# Create your models here.
class Discount(models.Model):

    TYPE = (
        ('Percentage Discount', 'Percentage Discount'),
        ('Payment Discount', 'Payment Discount')
    )
    
    name = models.CharField(max_length=50, db_index=True)
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
        return self.expiry >= now() and self.status

    @classmethod
    def auto_delete_expired(cls):
        expired_discounts = cls.objects.filter(models.Q(end_date__lt=now()) | models.Q(start_date__gt=now()), status=True)
        expired_discounts.update(status=False)


class Coupon(models.Model):

    TYPE = (
        ('Percentage Discount', 'Percentage Discount'),
        ('Payment Discount', 'Payment Discount')
    )
    
    code = models.CharField(max_length=25, unique=True, db_index=True)
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
        return self.expiry >= now() and self.status

    @classmethod
    def auto_delete_expired(cls):
        expired_coupons = cls.objects.filter(expiry__lt=now(), status=True)
        expired_coupons.update(status=False)

    class Meta:
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['expiry']),
        ]



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
    

class UsedCoupon(models.Model):

    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)