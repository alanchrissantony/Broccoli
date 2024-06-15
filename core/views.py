from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from product.models import Product
from category.models import Category
from accounts.models import Account
from user.models import Address, UserAddress, Country, State, City
from cart.views import discount_calculator, cart_id
from cart.models import CartItem, Cart
from order.models import Order, Payment, OrderProduct, OrderStatus
from promotion.models import Coupon
from user.views import verification_required
import datetime, paypalrestsdk
from django.db import transaction
from accounts.utils import send_mail
from django.http import JsonResponse
from wallet.models import Wallet, Transaction
from uuid import uuid4
from decimal import Decimal
from layout.models import Slide

# Create your views here.

paypalrestsdk.configure({
    'mode': 'sandbox',
    'client_id': "Abdh1FLUse82UfYoSfm3AmKWzYOpqbf46UW2E9y9bkW1LHraKhj2WKJoWhrHU7VMMZ3nGm4OsU1ai9O-",
    'client_secret': "EBURDNztUHjMcqiTukkZIPMkVnvf6f7gdZlzjifACW3mrye185tQqDFOTslpG5qFbCE63khmjRCvQBmt"
})

def order_product(request, cart_items, order, user, payment):
    for cart_item in cart_items:
        order_product = OrderProduct.objects.create(
            order=order,
            user=user,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price * cart_item.quantity,
            payment=payment,
            ordered=True
        )
        cart_item.product.stock -= order_product.quantity
        cart_item.product.save()

    cart_items.delete()
    email = request.user.email
    subject = f"Your order #{order.order_number}"
    content = "Thank you for your order! We’re excited to prepare your selection. You will receive a confirmation email with tracking information once your order ships. In the meantime, feel free to explore more delicious options on our app. If you have any questions, our support team is here to help. Happy dining!"
    send_mail(email, subject, content)

    return redirect('/orders/invoice/'+str(order.id))

def about(request):
    return render(request, 'public/user/about.html')

def coupon(request, wallet=None, wallet_pay=0, coupon=None, total=0, quantity=0, discount=0, vat=0, shipping=0, cart_items=None, coupon_code=None):
    coupon_code = request.GET.get('coupon')

    try:
        if request.user:
            wallet = Wallet.objects.filter(user=request.user).first()
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

    if wallet:
        if wallet.balance > price: 
            wallet_pay = price          
        else:
            wallet_pay = wallet.balance

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

            if 'wallet' in request.session:
                

                if wallet:
                    if wallet.balance > price: 
                        wallet_pay = price          
                        price = 0
                    else:
                        wallet_pay = wallet.balance
                        price -= float(wallet.balance)

            price = round(price, 2)

            context={
                'coupon':coupon.discount,
                'price':price,
                'wallet':wallet_pay
            }
            return JsonResponse(context)
        else:
            
            if 'coupon' in request.session:
                del request.session['coupon']
            
    if 'wallet' in request.session:
        
        
        if wallet:
            if wallet.balance > price: 
                wallet_pay = price          
                price = 0
            else:
                wallet_pay = wallet.balance
                price -= float(wallet.balance)
            price = round(price, 2)
                
                
    context={
        'coupon':None,
        'price':price,
        'wallet':wallet_pay,
    }
    return JsonResponse(context)
        
        

def wallet(request, wallet_pay=0, coupon_code=None, coupon=None, total=0, quantity=0, discount=0, vat=0, shipping=0, cart_items=None):
    status = request.GET.get('status')
    if 'coupon' in request.session:
        coupon_code = request.session['coupon']


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

    if coupon_code:
        coupon = Coupon.objects.filter(code=coupon_code).first()
        if coupon and price >= coupon.minimum_price:
            
            coupon_type = coupon.type
            coupon_discount = coupon.discount
            if coupon_type == 'Percentage Discount':
                price = round(price * (1 - coupon_discount / 100), 2)
            else:
                price = round(price - coupon_discount, 2)

    wallet = Wallet.objects.filter(user=request.user).first()

    if wallet:
        if status == 'true':
            request.session['wallet']=True
        else:
            del request.session['wallet']

        if wallet.balance > price:           
            wallet_pay = price
            if status == 'true':
                price = 0
        else:
            wallet_pay = wallet.balance
            if status == 'true':
                price -= float(wallet_pay)
    price = round(price, 2)
    context={
        'price':price,
        'wallet':wallet_pay
    }
    
    return JsonResponse(context)


@login_required(login_url='signin')
@verification_required
@transaction.atomic
def checkout(request):
    user = request.user
    cart = None
    cart_items = None
    address = None
    coupon = None
    wallet = None
    wallet_pay = None
    out_of_stock = None
    try:
        if user.id:
            cart_items = CartItem.objects.filter(user=user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
        discount = sum(discount_calculator(cart_item.product, cart_item.quantity) for cart_item in cart_items)
        vat = round((total * 18) / 100, 2)
        shipping = 15
        price = round(float(total + vat + shipping) - discount, 2)

        for cart_item in cart_items:
            if cart_item.product.stock < cart_item.quantity:
                out_of_stock = cart_item
    except Cart.DoesNotExist:
        total = 0
        discount = 0
        vat = 0
        shipping = 0
        price = 0
    
    if len(cart_items)<1:
        return redirect('cart')
    elif out_of_stock:
        messages.warning(request, "Unfortunately, some items in your cart are out of stock")
        return redirect('cart')

    if 'coupon' in request.session:
        coupon = Coupon.objects.filter(code=request.session.get('coupon')).first()
        
        if coupon and price >= coupon.minimum_price:
            coupon_type = coupon.type
            coupon_discount = coupon.discount
            if coupon_type == 'Percentage Discount':
                price = round(price * (1 - coupon_discount / 100), 2)
            else:
                price = round(price - coupon_discount, 2)
        else:
            del request.session['coupon']

    if 'wallet' in request.session:
            wallet = Wallet.objects.filter(user=request.user).first()

    if request.method == 'POST':
        addressId = request.POST.get('address')
        payment_metod = request.POST.get('payment_method')

        if addressId:
            address = Address.objects.get(id=addressId)
        else:
            address = UserAddress.objects.filter(user_id=user, is_default=True).first()
            if address:
                address = Address.objects.get(id=address.id)
            else:
                messages.warning(request, "Delivery address has not been selected!")
                return redirect('checkout')
    
        order = Order.objects.create(
            user=user,
            address=address,
            total=total,
            discount=float(discount),
            shipping=shipping,
            vat=vat,
            price=price,
            current_price=price,
            ip=request.META.get('REMOTE_ADDR'),
            order_number=generate_order_number()
        )
        if coupon:
            order.coupon = coupon
            order.save()
            del request.session['coupon']
        
        if wallet:
            if wallet.balance > price:           
                order.wallet = order.price
                wallet.balance -= Decimal(order.price)
            else:
                order.wallet = wallet.balance
                wallet.balance = 0
            del request.session['wallet']
            order.current_price = round(order.price - float(order.wallet), 2)
            Transaction.objects.create(
                transaction = uuid4(),
                user = wallet.user,
                amount = order.price,
                balance = wallet.balance,
                status = 'Debit'
            )
            wallet.save()
            order.save()

        request.session['order_id']=order.order_number
        if payment_metod == 'PayPal':
            return redirect('paypal_payment')
        else:
            payment = Payment.objects.create(
                user = request.user,
                payment_id = uuid4(),
                payment_method = 'Cash On Delivery',
                amount = order.price,
                status = 'Not Paid'
            )
            status, _ = OrderStatus.objects.get_or_create(name="Order Confirmed")
            order.statuses.add(status)
            order.is_ordered = True
            order.payment = payment
            if order.current_price <= 0:
                payment.status = 'Paid'
                payment.save()
            order.save()

        return order_product(request, cart_items, order, user, payment)

    countries = Country.objects.all()
    states = State.objects.all()
    cities = City.objects.all()

    user_address = UserAddress.objects.filter(user_id=user)
    
    if user_address:
        address = user_address

    if wallet:
        if wallet.balance > price:           
            wallet_pay = price
            price = 0
        else:
            wallet_pay = wallet.balance
            price -= float(wallet_pay)
        
    price = round(price, 2)

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
        'price': price,
        'coupon':coupon,
        'wallet':wallet_pay
    }

    return render(request, 'public/user/checkout.html', context)

def paypal_payment(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(order_number=order_id)

    total = order.current_price

    paypal_order = {
        'intent': 'sale',
        'payer':{
            'payment_method': 'paypal'
        },
        'redirect_urls':{
            'return_url': request.build_absolute_uri(reverse("paypal_success")),
            'cancel_url': request.build_absolute_uri(reverse("paypal_cancel"))
        },
        'transactions':[{
            'amount':{
                'total': str(total),
                'currency': 'USD',
            },
            'description': 'Payment for order #' + str(order_id)
        }]   
    }
    request.session['paypal_order'] = paypal_order
    return redirect('paypal_redirect')

def paypal_redirect(request):
    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET
    paypal_sdk_client = paypalrestsdk.Api({
        'mode': 'sandbox',
        'client_id': client_id,
        'client_secret': client_secret
    })

    paypal_order = request.session.get('paypal_order')
    paypal_order['redirect_urls']={
        'return_url': request.build_absolute_uri(reverse("paypal_success")),
        'cancel_url': request.build_absolute_uri(reverse("paypal_cancel"))
    }

    payment = paypalrestsdk.Payment(paypal_order)
    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                redirect_url = str(link.href)
                return redirect(redirect_url)
    else:
        messages.error(request, 'Payment processing failed. Please try again later')
        return redirect('checkout')
    
def paypal_success(request):
    payer_id = request.GET.get('PayerID')
    order_id = request.session.get('order_id')
    paypal_sdk_client = paypalrestsdk.Api({
        'mode': 'sandbox',
        'client_id': settings.PAYPAL_CLIENT_ID,
        'client_secret': settings.PAYPAL_CLIENT_SECRET
    })
    payment = paypalrestsdk.Payment.find(request.GET['paymentId'])
    if payment.execute({'payer_id':payer_id}):
        order = Order.objects.get(order_number=order_id)
        payment_obj = Payment.objects.create(
            user = request.user,
            payment_id = request.GET['paymentId'],
            payment_method = 'PayPal',
            amount = order.price,
            status = 'Paid'
        )
        status, _ = OrderStatus.objects.get_or_create(name="Order Confirmed")
        order.statuses.add(status)
        order.is_ordered = True
        order.payment = payment_obj

        order.save()

        del request.session['order_id']
        del request.session['paypal_order']

        user = Account.objects.get(id=request.user.id)
        cart_items = CartItem.objects.filter(user=user, is_active=True)

        messages.success(request, 'Payment processed successfully')
        return order_product(request, cart_items, order, user, payment_obj)
    else:
        messages.error(request, 'Payment processing failed. Please try again later')
        return redirect('checkout')

def paypal_cancel(request):
    messages.error(request, 'Payment was cancelled')
    return redirect('checkout')

def generate_order_number():
    today = datetime.date.today()
    return f"{today.strftime('%Y%m%d')}-{uuid4()}"

def comingsoon(request):
    return render(request, 'public/user/coming-soon.html')

def contact(request):
    return render(request, 'public/user/contact.html')

def faq(request):
    return render(request, 'public/user/faq.html')

def history(request):
    return render(request, 'public/user/history.html')

def home(request):
    
    categories = Category.objects.all().exclude(is_available=False)[:5]
    products_array = []
    for category in categories:  
        products_array.append(Product.objects.filter(category=category).exclude(is_available=False))
    products = Product.objects.all().exclude(is_available=False).order_by('-rating')[:12]
    slides = Slide.objects.all()

    context = {
        'categories':categories,
        'products_array':products_array,
        'products':products,
        'slides':slides
    }
    return render(request, 'public/user/index.html', context)


def location(request):
    return render(request, 'public/user/locations.html')
