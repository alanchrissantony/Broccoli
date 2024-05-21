from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.product, name="products"),
    path('<int:id>', views.productDetails, name="product_details"),
]