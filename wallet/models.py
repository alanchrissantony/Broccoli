from django.db import models
from accounts.models import Account

# Create your models here.
class Transaction(models.Model):

    STATUS = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    )
    transaction = models.CharField(max_length=50)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.transaction

class Wallet(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.user.username
