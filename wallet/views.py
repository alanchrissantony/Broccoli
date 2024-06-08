from django.shortcuts import render
from wallet.models import Wallet, Transaction
from uuid import uuid4

# Create your views here.

def create_wallet(user):
    Transaction.objects.create(transaction=uuid4(), user=user, amount=0, balance=0, status='Credit')

    wallet = Wallet.objects.create(
        user = user,
        balance = 0
    )
    return wallet
