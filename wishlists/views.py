from django.shortcuts import render, redirect
from accounts.models import Account
from product.models import Product
from wishlists.models import Wishlist
from django.contrib.auth.decorators import login_required
from user.views import verification_required

# Create your views here.

@login_required(login_url='signin')
@verification_required
def wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    context={
        'wishlists':wishlists
    }
    return render(request, 'public/user/wishlist.html', context)

@login_required(login_url='signin')
@verification_required
def add(request, id):
    try:
        wishlist = Wishlist.objects.get(user=request.user, product=id)
    except:
        user = Account.objects.get(email=request.user.email)
        product = Product.objects.get(id=id)
        wishlist = Wishlist.objects.create(user=user, product=product)
        wishlist.save()

    return redirect('wishlists')

@login_required(login_url='signin')
@verification_required
def remove(request, id):
    try:
        wishlist = Wishlist.objects.get(user=request.user, product=id)
        wishlist.delete()
    except:
        pass

    return redirect('wishlists')