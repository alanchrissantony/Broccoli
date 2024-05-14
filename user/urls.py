from django.urls import path, include
from . import views

urlpatterns = [
    path('account/', views.account, name="account"),
    path('signin/', views.signin, name="signin"),
    path('register/', views.register, name="register"),
    path('verification/', views.verification, name="verification"),
    path('alter/', views.password, name="paasword"),
]