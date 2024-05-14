from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('user/', include('user.urls')),
    path('about/', views.about, name="about"),
    path('products/', views.product, name="products"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('comingsoon/', views.comingsoon, name="comingsoon"),
    path('contact/', views.contact, name="contact"),
    path('faq/', views.faq, name="faq"),
    path('history/', views.history, name="history"),
    path('location/', views.location, name="location"),
    path('order/', views.order, name="order"),
    path('order/tracking', views.tracking, name="tracking"),
    path('product/details', views.product_details, name="product_details"),
    path('wishlist/', views.wishlist, name="wishlist"),
]