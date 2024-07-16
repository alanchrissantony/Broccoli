from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('', cache_page(60 * 15)(views.product), name="products"),
    path('<int:id>', cache_page(60 * 15)(views.productDetails), name="product_details"),
]