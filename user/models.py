from django.db import models
from accounts.models import Account
from phonenumber_field.modelfields import PhoneNumberField
import uuid

# Create your models here.
class Country(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('name',)

    def __str__(self):
        return self.name

class State(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class City(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ('name',)
    
    def __str__(self):
        return self.name

class Address(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=25)
    address = models.CharField(max_length=255, blank=True)
    additional = models.CharField(max_length=255, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    zip_code = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    order_instruction = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.first_name    

class UserAddress(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)
