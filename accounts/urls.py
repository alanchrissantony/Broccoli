from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.root, name="root"),
    path('api/chart/', views.chart, name="chart"),
    path('login/', views.Authentication.signin, name="root_signin"),
    path('signup/', views.Authentication.signup, name="root_signup"),
    path('signout/', views.Authentication.signout, name="root_signout"),
    path('products/', views.Products.products, name="root_products"),
    path('products/add', views.Products.add, name="root_add_products"),
    path('products/edit/<int:id>', views.Products.edit, name="root_edit_products"),
    path('products/delete/<int:id>', views.Products.delete, name="root_delete_products"),
    path('products/delete/images/<int:id>', views.Products.delete_image, name="root_delete_products_image"),
    path('layouts', views.layout, name="root_layouts"),
    path('users', views.Users.users, name="root_users"),
    path('users/add', views.Users.add, name="root_add_user"),
    path('users/edit/<int:id>', views.Users.edit, name="root_edit_user"),
    path('users/delete/<int:id>', views.Users.delete, name="root_delete_user"),
    path('categories/', include('category.urls')),
    path('orders', views.Orders.orders, name="root_orders"),
    path('orders/edit/<int:id>', views.Orders.edit, name="root_edit_orders"),
    path('orders/cancel/<int:id>', views.Orders.cancel, name="root_cancel_orders"),
    path('orders/delete/<int:id>', views.Orders.delete, name="root_delete_orders"),
    path('orders/cancel', views.Orders.cancellation, name="root_cancellation_orders"),
    path('wallets', views.UserWallet.user_wallet, name="root_wallet"),
    path('wallets/<int:id>', views.UserWallet.view, name="root_user_wallet"),
    path('discounts', views.ProductPromotion.ProductDiscount.product_discount, name="root_discounts"),
    path('discounts/add', views.ProductPromotion.ProductDiscount.add, name="root_add_discounts"),
    path('discounts/edit/<int:id>', views.ProductPromotion.ProductDiscount.edit, name="root_edit_discounts"),
    path('discounts/delete/<int:id>', views.ProductPromotion.ProductDiscount.delete, name="root_delete_discounts"),
    path('coupons', views.ProductPromotion.ProductCoupon.product_coupon, name="root_coupons"),
    path('coupons/add', views.ProductPromotion.ProductCoupon.add, name="root_add_coupons"),
    path('coupons/edit/<int:id>', views.ProductPromotion.ProductCoupon.edit, name="root_edit_coupons"),
    path('coupons/delete/<int:id>', views.ProductPromotion.ProductCoupon.delete, name="root_delete_coupons"),
    path('promotions/products', views.ProductPromotion.ProductPromotion.product_promotion, name="root_product_promotions"),
    path('promotions/products/add', views.ProductPromotion.ProductPromotion.add, name="root_add_product_promotions"),
    path('promotions/products/edit/<int:id>', views.ProductPromotion.ProductPromotion.edit, name="root_edit_product_promotions"),
    path('promotions/products/delete/<int:id>', views.ProductPromotion.ProductPromotion.delete, name="root_delete_product_promotions"),
    path('promotions/categories', views.ProductPromotion.CategoryPromotion.category_promotion, name="root_category_promotions"),
    path('promotions/categories/add', views.ProductPromotion.CategoryPromotion.add, name="root_add_category_promotions"),
    path('promotions/categories/edit/<int:id>', views.ProductPromotion.CategoryPromotion.edit, name="root_edit_category_promotions"),
    path('promotions/categories/delete/<int:id>', views.ProductPromotion.CategoryPromotion.delete, name="root_delete_category_promotions"),
]