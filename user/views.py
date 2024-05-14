from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages

# Create your views here.
def account(request):
    return render(request, 'public/user/account.html')

def password(request):
    return render(request, 'public/user/password.html')

def signin(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user=authenticate(email, password)

        
    return render(request, 'public/user/login.html')

def register(request):
    return render(request, 'public/user/register.html')

def verification(request):
    return render(request, 'public/user/verification.html')