from django.shortcuts import render, redirect
from order.models import OrderProduct
from django.core.paginator import Paginator
from wallet.models import Wallet, Transaction
from django.contrib.auth.decorators import login_required
from user.views import verification_required
from uuid import uuid4

# Create your views here.
@login_required(login_url='signin')
@verification_required
def order(request):
    products = OrderProduct.objects.filter(user=request.user).order_by('-created_at')
    items_per_page = 10
    paginator = Paginator(products, items_per_page)

    page = request.GET.get('page')
    obj = paginator.get_page(page)

    context = {
        'products':obj
    }
    return render(request, 'public/user/order.html', context)

def delete(request, id):
    try:
        order = OrderProduct.objects.get(order=id)
        print(order.order_number)
        if order.payment.status == 'Paid':
            wallet = Wallet.objects.get(user=request.user)
            Transaction.objects.create(
                transaction = uuid4(),
                user = wallet.user,
                amount = order.price,
                balance = wallet.balance + order.price,
                status = 'Credit'
            )
            wallet.balance += order.price
            wallet.save()

        order.product.stock += order.quantity
        order.product.save()
        order.delete()
    except:
        pass
    return redirect('orders')

def tracking(request):
    return render(request, 'public/user/order-tracking.html')

def invoice(request, id):
    return render(request, 'public/user/invoice.html')