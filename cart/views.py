from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from product.models import Product
from cart.models import Cart, CartItem
from promotion.models import Coupon
from promotion.models import Promotion, PromotionCategory
from django.contrib.auth.decorators import login_required
import json



# Create your views here.
def discount_calculator(product, quantity):

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

        if category_discount_type == 'percentage':
            discount += category_discount_value
        else:
            reduction += category_discount_value  # Limit amount discount to product price

    # Apply combined discount to price
    return round(((price * discount / 100)+ reduction)*quantity, 2)


def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@login_required(login_url='signin')
def add(request, product_id, quantity):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product_id=product, cart_id=cart)
        cart_item.quantity += quantity
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=quantity, cart=cart, user=request.user)
        cart_item.save()

    return redirect('cart')
    
@login_required(login_url='signin')
def remove(request, product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required(login_url='signin')
def delete(request, product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect('cart')

@login_required(login_url='signin')
def cart(request, total=0, quantity=0, discount=0, vat=0, shipping=0, cart_items=None, coupon=None):
    
    try:
        if request.user:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True) 
        else: 
            cart = Cart.objects.get(cart_id=cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            discount += discount_calculator(cart_item.product, cart_item.quantity)
            quantity += cart_item.quantity

        vat = round((total*18)/100, 2)
        shipping = 15
        price = round(float(total+vat+shipping) - discount, 2)
    except:
        
        pass

    coupon_code = request.GET.get('coupon')
    
    if coupon_code:
        coupon = Coupon.objects.filter(code=coupon_code).first()
        if coupon and price >= coupon.minimum_price:
            request.session['coupon']=coupon.code
            
            coupon_type = coupon.type
            coupon_discount = coupon.discount
            if coupon_type == 'Percentage Discount':
                price = round(price * (1 - coupon_discount / 100), 2)
            else:
                price = round(price - coupon_discount, 2)

            context={
                'coupon':coupon.discount,
                'price':price
            }
            return JsonResponse(context)
        else:
            if 'coupon' in request.session:
                del request.session['coupon']

            context={
                'coupon':0,
                'price':price
            }
            return JsonResponse(context)
    context={
        'total':total,
        'quantity':quantity,
        'discount':discount,
        'cart_items':cart_items,
        'shipping':shipping,
        'vat':vat,
        'price': price

    }

    return render(request, 'public/user/cart.html', context)