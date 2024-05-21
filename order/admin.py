from django.contrib import admin
from order.models import Order, Payment, OrderProduct, OrderStatus

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'total', 'discount', 'price', 'is_ordered', 'created_at']
    list_filter = ['statuses', 'is_ordered']
    search_fields = ['order_number']
    list_per_page = 20
    inlines = [OrderProductInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "statuses":
            # Retrieve the choices from the OrderStatus model
            kwargs["queryset"] = OrderStatus.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(OrderStatus)

