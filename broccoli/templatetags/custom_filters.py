# custom_filters.py
from django import template
from promotion.models import Promotion, PromotionCategory, Discount

register = template.Library()

@register.filter(name="calculate_discounted_price")
def calculate_discounted_price(product):
    price = float(product.price)
    try:
        product_discount = Promotion.objects.get(product=product).discount.discount
    except:
        product_discount = 0.00
    try:
        category_discount = PromotionCategory.objects.get(category=product.category).discount.discount
    except:
        category_discount = 0


    discount = product_discount+category_discount
    return round(price * (1 - discount / 100), 2)


@register.filter(name="product_discount")
def product_discount(product):
    try:
        product_discount = Promotion.objects.get(product=product).discount.discount
    except:
        product_discount = 0.00
    try:
        category_discount = PromotionCategory.objects.get(category=product.category).discount.discount
    except:
        category_discount = 0


    discount = product_discount+category_discount
    return discount


@register.filter(name="category_discount")
def category_discount(category):

    try:
        discount = PromotionCategory.objects.get(category=category).discount.discount
    except:
        discount = 0

    return discount

@register.filter
def last_item(queryset):
    return queryset.last()


@register.filter
def page_number_start(queryset):
    return ((queryset-1)*9)+1

@register.filter
def page_number_end(queryset):
    return queryset*9
