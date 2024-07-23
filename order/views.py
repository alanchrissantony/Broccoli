from django.shortcuts import render, redirect
from order.models import OrderProduct, Order, Review, OrderCancel, OrderStatus
from django.core.paginator import Paginator
from wallet.models import Wallet, Transaction
from django.contrib.auth.decorators import login_required
from user.views import verification_required
from product.models import Product
from accounts.models import Account
from uuid import uuid4
from decimal import Decimal
from django.contrib import messages

# Create your views here.
@login_required(login_url='signin/')
@verification_required
def order(request, id):

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('review')
        product_id = request.POST.get('product')
        order_id = request.POST.get('order')

        product = Product.objects.get(id=product_id)
        order_obj = Order.objects.get(id=order_id)

        review = Review.objects.filter(order=order_obj).first()
        if review:
            review.rating=rating
            review.comment=comment
            review.save()
        else:
            Review.objects.create(
                product = product,
                user = order_obj.user,
                order = order_obj,
                rating = rating,
                comment = comment,
            )
        reviews = Review.objects.filter(product=product)
        if not reviews:
            return 0
        total_rating = sum(review.rating for review in reviews)
        product.rating = total_rating / len(reviews)
        product.save()
        
    orders = Order.objects.filter(id=id).first()
    products = OrderProduct.objects.filter(order=id).order_by('-created_at')
    items_per_page = 10
    paginator = Paginator(products, items_per_page)

    page = request.GET.get('page')
    obj = paginator.get_page(page)

    context = {
        'order':orders,
        'products':obj
    }
    return render(request, 'public/user/order.html', context)

def delete(request, id):
    try:
        order = Order.objects.get(id=id)
        products = OrderProduct.objects.filter(order=order)
        if order.payment.status == 'Paid':
            wallet = Wallet.objects.get(user=request.user)
            Transaction.objects.create(
                transaction = uuid4(),
                user = wallet.user,
                amount = order.price,
                balance = float(wallet.balance) + order.price,
                status = 'Credit'
            )
            wallet.balance += Decimal(order.price)
            wallet.save()
        cancel = OrderCancel.objects.create(order=order)
        for product in products:
            product.product.stock += product.quantity
            product.product.save()
        last_status = order.statuses.last().name
        if last_status == 'Order Confirmed':
            status, _ = OrderStatus.objects.get_or_create(name='Shipped')
            order.statuses.add(status)
            last_status = 'Shipped'
        
        if last_status == 'Shipped':
            status, _ = OrderStatus.objects.get_or_create(name='Out for delivery')
            order.statuses.add(status)
        status, _ = OrderStatus.objects.get_or_create(name='Cancelled')
        order.statuses.add(status)
        order.save()
    
    except:
        pass
    return redirect('account')

@login_required(login_url='signin/')
@verification_required
def tracking(request):
    if request.method == "POST":
        number = request.POST.get('number')
        email = request.POST.get('email')

        user = Account.objects.filter(email=email).first()
        
        if user:
            order = Order.objects.filter(order_number=number, user=user).first()
            if order:
                return redirect(f'/orders/{order.id}')
            messages.error(request, "Invalid credentials!")
        else:
            messages.error(request, "Invalid email!")
        
    return render(request, 'public/user/order-tracking.html')

@login_required(login_url='signin/')
@verification_required
def invoice(request, id):
    order = Order.objects.filter(id=id).first()
    products = OrderProduct.objects.filter(order=id).order_by('-created_at')
    context = {
        'order':order,
        'products':products
    }
    return render(request, 'public/user/invoice.html', context)