from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('user/', include('user.urls')),
    path('products/', include('product.urls')),
    path('root/', include('accounts.urls')),
    path('about/', views.about, name="about"),
    path('cart/', include('cart.urls')),
    path('checkout/', views.checkout, name="checkout"),
    path('comingsoon/', views.comingsoon, name="comingsoon"),
    path('contact/', views.contact, name="contact"),
    path('faq/', views.faq, name="faq"),
    path('history/', views.history, name="history"),
    path('location/', views.location, name="location"),
    path('orders/', include('order.urls')),
    path('wishlists/', include('wishlists.urls')),
    path('api/wallet/', views.wallet, name="wallet"),
    path('api/coupon', views.coupon, name="coupon"),
    path('paypal/payment', views.paypal_payment, name="paypal_payment"),
    path('paypal/redirect', views.paypal_redirect, name="paypal_redirect"),
    path('paypal/success', views.paypal_success, name="paypal_success"),
    path('paypal/cancel', views.paypal_cancel, name="paypal_cancel"),
]