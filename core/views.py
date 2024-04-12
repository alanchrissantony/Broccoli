from django.shortcuts import render

# Create your views here.

def about(request):
    return render(request, 'public/about.html')

def account(request):
    return render(request, 'public/account.html')

def cart(request):
    return render(request, 'public/cart.html')

def checkout(request):
    return render(request, 'public/checkout.html')

def comingsoon(request):
    return render(request, 'public/coming-soon.html')

def contact(request):
    return render(request, 'public/contact.html')

def faq(request):
    return render(request, 'public/faq.html')

def history(request):
    return render(request, 'public/history.html')

def index(request):
    return render(request, 'public/index.html')

def location(request):
    return render(request, 'public/locations.html')

def signin(request):
    return render(request, 'public/login.html')

def order(request):
    return render(request, 'public/order-tracking.html')

def product_details(request):
    return render(request, 'public/product-details.html')

def register(request):
    return render(request, 'public/register.html')

def product(request):
    return render(request, 'public/products.html')

def wishlist(request):
    return render(request, 'public/wishlist.html')