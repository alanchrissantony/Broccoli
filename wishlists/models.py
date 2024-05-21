from django.db import models
from product.models import Product
from accounts.models import Account


# Create your models here.
class Wishlist(models.Model):
    
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name