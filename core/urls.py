from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('account/', views.account, name="account"),
    path('products/', views.product, name="products"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('comingsoon/', views.comingsoon, name="comingsoon"),
    path('contact/', views.contact, name="contact"),
    path('faq/', views.faq, name="faq"),
    path('history/', views.history, name="history"),
    path('location/', views.location, name="location"),
    path('signin/', views.signin, name="signin"),
    path('order/tracking', views.order, name="order_tracking"),
    path('product/details', views.product_details, name="product_details"),
    path('register/', views.register, name="register"),
    path('wishlist/', views.wishlist, name="wishlist"),
]