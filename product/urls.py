from django.urls import path

urlpatterns = [
    path('', name="products"),
    path('<int:id>', name="product_details"),
]