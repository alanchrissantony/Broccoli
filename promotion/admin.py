from django.contrib import admin
from promotion.models import Discount, Coupon, Promotion, PromotionCategory
# Register your models here.

admin.site.register(Coupon)
admin.site.register(Discount)
admin.site.register(Promotion)
admin.site.register(PromotionCategory)