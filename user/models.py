from django.db import models
from accounts.models import Account
from phonenumber_field.modelfields import PhoneNumberField
from functools import partial
from core.models import image_upload_path


# Create your models here.
class Country(models.Model):
    
    name = models.CharField(max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('name',)

    def __str__(self):
        return self.name

class State(models.Model):
    
    name = models.CharField(max_length=50, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class City(models.Model):
    
    name = models.CharField(max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ('name',)
    
    def __str__(self):
        return self.name

class Address(models.Model):
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, db_index=True)
    address = models.CharField(max_length=255, blank=True)
    additional = models.CharField(max_length=255, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    zip_code = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    order_instruction = models.TextField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.first_name    

class UserAddress(models.Model):
    
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User Address'
        verbose_name_plural = 'User Addresses'


class Avatar(models.Model):

    image = models.ImageField(upload_to=partial(image_upload_path, folder='avatars'), blank=True)