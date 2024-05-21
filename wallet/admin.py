from django.contrib import admin
from wallet.models import Wallet, Transaction

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Transaction)