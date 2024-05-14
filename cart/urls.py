from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('add/<int:product_id>/<int:quantity>/', views.add, name="add_cart"),
    path('remove/<int:product_id>', views.remove, name="remove_cart"),
    path('delete/<int:product_id>', views.delete, name="delete_cart"),
]