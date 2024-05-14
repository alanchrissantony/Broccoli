from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from product.models import Product
from category.models import Category
from accounts.models import Account
from user.models import Address, UserAddress, Country, State, City
from cart.views import discount_calculator, cart_id
from cart.models import CartItem, Cart
from order.models import Order, Payment, OrderProduct, OrderStatus
import datetime
from django.db import transaction
import json

# Create your views here.

def about(request):
    return render(request, 'public/user/address.html')

@login_required(login_url='signin')
@transaction.atomic
def checkout(request):
    user = request.user
    cart = None
    cart_items = None
    address = None

    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
        discount = sum(discount_calculator(cart_item.product, cart_item.quantity) for cart_item in cart_items)
        vat = round((total * 18) / 100, 2)
        shipping = 15
        price = round(float(total + vat + shipping) - discount, 2)
    except Cart.DoesNotExist:
        total = 0
        discount = 0
        vat = 0
        shipping = 0
        price = 0

    if request.method == 'POST':
        addressId = request.POST.get('address')
        if addressId:
            address = Address.objects.get(id=addressId)
        else:
            address = UserAddress.objects.get(user_id=user, is_default=True)
            address = Address.objects.get(id=address.id)
    
        order = Order.objects.create(
            user=user,
            address=address,
            total=total,
            discount=float(discount),
            shipping=shipping,
            vat=vat,
            price=price,
            ip=request.META.get('REMOTE_ADDR'),
            order_number=generate_order_number()
        )

        status, _ = OrderStatus.objects.get_or_create(name="Order Confirmed")
        order.statuses.add(status)

        for cart_item in cart_items:
            order_product = OrderProduct.objects.create(
                order=order,
                user=user,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price * cart_item.quantity,
                ordered=True
            )
            cart_item.product.stock -= order_product.quantity
            cart_item.product.save()

        cart_items.delete()

        return redirect('orders')

    countries = Country.objects.all()
    states = State.objects.all()
    cities = City.objects.all()

    user_address = UserAddress.objects.filter(user_id=user)
    
    if user_address:
        address = user_address

    context = {
        'address': address,
        'user': user,
        'countries': countries,
        'states': states,
        'cities': cities,
        'total': total,
        'discount': discount,
        'shipping': shipping,
        'vat': vat,
        'price': price
    }

    return render(request, 'public/user/checkout.html', context)

def generate_order_number():
    today = datetime.date.today()
    return f"{today.strftime('%Y%m%d')}{today.strftime('%H%M%S')}"

def comingsoon(request):
    return render(request, 'public/user/coming-soon.html')

def contact(request):
    return render(request, 'public/user/contact.html')

def faq(request):
    return render(request, 'public/user/faq.html')

def history(request):
    return render(request, 'public/user/history.html')

@login_required(login_url='signin')
def home(request):
    
    user = request.user

    if not user.is_verified:
        return redirect('verification')

    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories':categories,
        'products':products
    }
    return render(request, 'public/user/index.html', context)


def location(request):
    return render(request, 'public/user/locations.html')

def wishlist(request):
    return render(request, 'public/user/wishlist.html')