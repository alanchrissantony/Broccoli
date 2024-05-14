from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from cart.models import Cart, CartItem
from category.models import Category
from promotion.models import Promotion, PromotionCategory
from django.contrib.auth.decorators import login_required



# Create your views here.
def discount_calculator(product, quantity):

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
    return round((price * discount / 100)*quantity, 2)


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
    return redirect("cart")
    
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
def cart(request, total=0, quantity=0, discount=0, vat=0, shipping=0, cart_items=None):
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

        vat = (total*18)/100
        shipping = 15
    except:
        
        pass

    context={
        'total':total,
        'quantity':quantity,
        'discount':discount,
        'cart_items':cart_items,
        'shipping':shipping,
        'vat':vat,
        'price': round(float(total+vat+shipping) - discount, 2)

    }
    return render(request, 'public/user/cart.html', context)