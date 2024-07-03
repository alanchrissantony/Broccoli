from django.db import models
from accounts.models import Account
from product.models import Product
from user.models import Address
from promotion.models import Coupon


# Create your models here.

class Payment(models.Model):
    
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255, null=True, db_index=True)
    payment_method = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    
class OrderStatus(models.Model):
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    
    name = models.CharField(max_length=20, choices=STATUS)

    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'statuses'

    def __str__(self):
        return self.name

class Order(models.Model):
    
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=50, db_index=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.FloatField()
    price = models.FloatField()
    wallet = models.FloatField(default=0)
    current_price = models.FloatField()
    shipping = models.FloatField()
    vat = models.FloatField()
    statuses = models.ManyToManyField(OrderStatus)
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)


class OrderProduct(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField()
    comment = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
    
class OrderCancel(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order.order_number