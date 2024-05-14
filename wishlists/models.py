from django.db import models
from product.models import Product
from accounts.models import Account

# Create your models here.
class Wishlist(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)