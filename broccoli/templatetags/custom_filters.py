# custom_filters.py
from django import template
from promotion.models import Promotion, PromotionCategory
from wishlists.models import Wishlist
from order.models import Review

register = template.Library()

@register.filter(name="calculate_discounted_price")
def calculate_discounted_price(product):
    price = float(product.price)
    discount = 0.00
    reduction = 0

    # Get active product and category promotions (handle potential absence)
    product_promotion = Promotion.objects.filter(product=product).first()
    category_promotion = PromotionCategory.objects.filter(category=product.category).first()
    
    # Calculate discount based on promotion type if existing
    if product_promotion:
        discount_type = product_promotion.discount.type
        discount_value = product_promotion.discount.discount
        
        if discount_type == 'Percentage Discount':
            discount += discount_value
        else:
            reduction += discount_value # Limit amount discount to product price
    
    if category_promotion:
        category_discount_type = category_promotion.discount.type
        category_discount_value = category_promotion.discount.discount

        if category_discount_type == 'Percentage Discount':
            discount += category_discount_value
        else:
            reduction += category_discount_value  # Limit amount discount to product price

    # Apply combined discount to price
    return round(price * (1 - discount / 100) - reduction, 2)


@register.filter(name="product_discount")
def product_discount(product):
    try:
        product_discount = Promotion.objects.get(product=product).discount.discount
    except:
        product_discount = 0.00

    discount = product_discount
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

@register.filter
def in_wishlist(product, user):  # Include user as an argument
    wishlist = Wishlist.objects.filter(product=product, user=user).first()

    if wishlist:
        return True
    return False

@register.filter(name='custom_range')
def custom_range(end):
    return range(1, end + 1)

@register.filter(name='custom_conventer')
def custom_conventer(val):
    return round(val/1000, 2)

@register.filter(name='get_item')
def get_item(dict, key):
    return dict[key]
