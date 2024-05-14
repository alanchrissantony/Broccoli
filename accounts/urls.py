from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.root, name="root"),
    path('signin/', views.Authentication.signin, name="root_signin"),
    path('signup/', views.Authentication.signup, name="root_signup"),
    path('signout/', views.Authentication.signout, name="root_signout"),
    path('products/', views.Products.products, name="root_products"),
    path('products/add', views.Products.add, name="root_add_products"),
    path('products/edit/<int:id>', views.Products.edit, name="root_edit_products"),
    path('products/delete/<int:id>', views.Products.delete, name="root_delete_products"),
    path('products/delete/images/<int:id>', views.Products.delete_image, name="root_delete_products_image"),
    path('users', views.Users.users, name="root_users"),
    path('users/add', views.Users.add, name="root_add_user"),
    path('users/edit/<int:id>', views.Users.edit, name="root_edit_user"),
    path('users/delete/<int:id>', views.Users.delete, name="root_delete_user"),
    path('categories/', include('category.urls')),
    path('carts', views.Carts.carts, name="root_carts"),
    path('orders', views.Orders.orders, name="root_orders"),
    path('orders/edit/<int:id>', views.Orders.edit, name="root_edit_orders"),
    path('orders/delete/<int:id>', views.Orders.delete, name="root_delete_orders"),
]