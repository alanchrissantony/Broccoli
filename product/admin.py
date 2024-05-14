from django.contrib import admin
from product.models import  Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'modified_at', 'is_available')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
