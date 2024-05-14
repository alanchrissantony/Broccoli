from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.order, name="orders"),
    path('tracking', views.tracking, name="tracking"),
    path('details/<int:id>', views.order, name="order_details"),
    path('delete/<int:id>', views.delete, name="delete_order"),
]