from django.db import models
from product.models import Product
from accounts.models import Account
import uuid

# Create your models here.
class Wishlist(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)