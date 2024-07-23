from django.shortcuts import render, redirect
from accounts.models import Account
from product.models import Product
from wishlists.models import Wishlist
from django.contrib.auth.decorators import login_required
from user.views import verification_required
from django.views.decorators.cache import cache_control
from django.core.cache import cache

# Create your views here.

@login_required(login_url='signin')
@verification_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
    cache.delete(f'product_{id}')
    cache.delete(f'related_products_{id}')

    return redirect('wishlists')

@login_required(login_url='signin')
@verification_required
def remove(request, id):
    try:
        wishlist = Wishlist.objects.get(user=request.user, product=id)
        wishlist.delete()
    except:
        pass
    cache.delete(f'product_{id}')
    cache.delete(f'related_products_{id}')
    return redirect('wishlists')