from django.shortcuts import render

# Create your views here.

def about(request):
    return render(request, 'public/user/about.html')

def cart(request):
    return render(request, 'public/user/cart.html')

def checkout(request):
    return render(request, 'public/user/checkout.html')

def comingsoon(request):
    return render(request, 'public/user/coming-soon.html')

def contact(request):
    return render(request, 'public/user/contact.html')

def faq(request):
    return render(request, 'public/user/faq.html')

def history(request):
    return render(request, 'public/user/history.html')

def index(request):
    return render(request, 'public/user/index.html')

def location(request):
    return render(request, 'public/user/locations.html')

def order(request):
    return render(request, 'public/user/order.html')

def tracking(request):
    return render(request, 'public/user/order-tracking.html')

def product_details(request):
    return render(request, 'public/user/product-details.html')

def product(request):
    return render(request, 'public/user/products.html')

def wishlist(request):
    return render(request, 'public/user/wishlist.html')