from django.contrib import admin
from user.models import Country, State, City, Address, UserAddress, Avatar

# Register your models here.
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(UserAddress)
admin.site.register(Avatar)