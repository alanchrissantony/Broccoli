from cart.models import Cart, CartItem
from cart.views import cart_id
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def CartCounter(request, total=0, quantity=0):
    
    user = request.user
    if user:
        cart_items = CartItem.objects.filter(user=user, is_active=True)
    else:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    context = {
        'cart_view':cart_items,
        'cart_quantity':quantity,
        'cart_total':total
    }
    return context