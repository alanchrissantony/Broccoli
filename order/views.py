from django.shortcuts import render, redirect
from order.models import OrderProduct
from django.core.paginator import Paginator

# Create your views here.
def order(request):
    products = OrderProduct.objects.filter(user=request.user)
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
        order.product.stock += order.quantity
        order.product.save()
        order.delete()
    except:
        pass
    return redirect('orders')

def tracking(request):
    return render(request, 'public/user/order-tracking.html')