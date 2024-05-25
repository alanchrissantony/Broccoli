from django.shortcuts import render, redirect
from order.models import OrderProduct, Order, Review
from django.core.paginator import Paginator
from wallet.models import Wallet, Transaction
from django.contrib.auth.decorators import login_required
from user.views import verification_required
from product.models import Product
from accounts.models import Account
from uuid import uuid4
from decimal import Decimal

# Create your views here.
@login_required(login_url='signin')
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
        
        for product in products:
            product.product.stock += product.quantity
            product.product.save()
            product.delete()
        order.delete()
    
    except:
        pass
    return redirect('account')

def tracking(request):
    return render(request, 'public/user/order-tracking.html')

def invoice(request, id):
    order = Order.objects.filter(id=id).first()
    products = OrderProduct.objects.filter(order=id).order_by('-created_at')
    context = {
        'order':order,
        'products':products
    }
    return render(request, 'public/user/invoice.html', context)