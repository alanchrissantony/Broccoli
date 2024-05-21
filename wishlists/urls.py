from django.urls import path
from wishlists import views

urlpatterns = [
    path('', views.wishlist, name="wishlists"),
    path('add/<int:id>', views.add, name="wishlists_add"),
    path('remove/<int:id>', views.remove, name="wishlists_remove"),
]