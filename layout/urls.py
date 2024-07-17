from django.urls import path
from layout import views

urlpatterns = [
    path('', views.layout, name="root_layouts"),
]