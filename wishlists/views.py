from django.shortcuts import render, redirect
from accounts.models import Account
from product.models import Product
from wishlists.models import Wishlist

# Create your views here.


def wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    context={
        'wishlists':wishlists
    }
    return render(request, 'public/user/wishlist.html', context)

def add(request, id):
    try:
        wishlist = Wishlist.objects.get(user=request.user, product=id)
    except:
        user = Account.objects.get(email=request.user.email)
        product = Product.objects.get(id=id)
        wishlist = Wishlist.objects.create(user=user, product=product)
        wishlist.save()

    return redirect('wishlists')

def remove(request, id):
    print(112114)
    try:
        wishlist = Wishlist.objects.get(user=request.user, product=id)
        wishlist.delete()
    except:
        pass

    return redirect('wishlists')