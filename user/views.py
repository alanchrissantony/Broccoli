from django.shortcuts import render, redirect
from django.contrib import messages, auth
from accounts.models import Account
from accounts.tests import JsonEncoder
from accounts.validator import Validator
from cart.models import Cart, CartItem
from cart.views import cart_id
from user.models import Address, UserAddress, Country, State, City
from accounts import otp
import json

# Create your views here.


def account(request):
    return render(request, 'public/user/account.html')

def password(request):
    return render(request, 'public/user/password.html')

def signin(request):
    if 'user' in request.session:
        return redirect('home')
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email, password=password)

        if user:
            try:
                cart = Cart.objects.get(cart_id=cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request, user)
            request.session['user']=json.dumps(user, cls=JsonEncoder)
            return redirect('verification')
            
        messages.error(request, 'Invalid credentials')
        return redirect('signin')
        
    return render(request, 'public/user/login.html')

def register(request):
    if 'user' in request.session:
        return redirect('home')
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        username = email.split('@')[0]
        
        if password == confirm_password:
            if (Validator.validate_name(first_name)):
                messages.error(request, 'Please enter a valid first name.')
            elif(Validator.validate_name(last_name)):
                messages.error(request, 'Please enter a valid last name.')
            elif(Validator.validate_email(email)):
                messages.error(request, 'Please enter a valid email UserAddress.')
            elif(Validator.validate_password(password)):
                messages.error(request, 'The password must contain at least 8 characters, including at least one letter, one digit, and one special character (@$!%*?&).')
            else:
                try:
                    user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    messages.success(request, "User has been successfully created.!")
                    request.session['user']=json.dumps(user, cls=JsonEncoder)
                    return redirect('home')
                except:
                    messages.error(request, 'User already exists!')
        else:
            messages.error(request, "The passwords provided do not match!")

    return render(request, 'public/user/register.html')

def signout(request):
    auth.logout(request)
    request.session.clear()
    return redirect('signin')

def verification(request):
    if 'user' in request.session:
        user = request.user
        
        if not user.is_verified:

            if request.method == 'POST':
                otp_secret = request.POST['otp']

                verify = otp.verify(request, otp_secret)
                if verify:
                    user = Account.objects.get(email=user.email)
                    user.is_verified=True
                    user.save()
                    request.session['user']=json.dumps(user, cls=JsonEncoder)
                    return redirect('home')
                messages.error(request, 'Invalid OTP')

            otp_key = otp.send(request, user.email)
            context={
                'email':user.email
            }         
            return render(request, 'public/user/verification.html', context)
    return redirect('signin')

class AddressUser:

    def add(request):
        user = request.user
        if request.method == 'POST':
            form_data = request.POST

            address_data = {
                'first_name': form_data.get('firstname'),
                'last_name': form_data.get('lastname'),
                'email': form_data.get('email'),
                'phone_number': form_data.get('phone'),
                'address': form_data.get('address'),
                'additional': form_data.get('additional'),
                'city': City.objects.get(name=form_data.get('city')),
                'state': State.objects.get(name=form_data.get('state')),
                'zip_code': form_data.get('zip_code'),
                'order_instruction': form_data.get('message'),
                'country': Country.objects.get(name=form_data.get('country'))
            }

            
            address_instance = Address.objects.create(**address_data)
            user_address = UserAddress.objects.create(user_id=user, address_id=address_instance)

            return redirect('checkout')
        countries = Country.objects.all()
        states = State.objects.all()
        cities = City.objects.all()

        context = {
            'countries': countries,
            'states': states,
            'cities': cities,
        }
        return render(request, "public/user/address.html", context)
    
    def edit(request, id):
        user = request.user
        if request.method == 'POST':
            form_data = request.POST

            address_data = {
                'first_name': form_data.get('firstname'),
                'last_name': form_data.get('lastname'),
                'email': form_data.get('email'),
                'phone_number': form_data.get('phone'),
                'address': form_data.get('address'),
                'additional': form_data.get('additional'),
                'city': City.objects.get(name=form_data.get('city')),
                'state': State.objects.get(name=form_data.get('state')),
                'zip_code': form_data.get('zip_code'),
                'order_instruction': form_data.get('message'),
                'country': Country.objects.get(name=form_data.get('country'))
            }

            user_address = UserAddress.objects.filter(address_id=id).first()
            if user_address:
                address_instance = user_address.address_id
                for key, value in address_data.items():
                    setattr(address_instance, key, value)
                address_instance.save()
            else:
                address_instance = Address.objects.create(**address_data)
                user_address = UserAddress.objects.create(user_id=user, address_id=address_instance)

            return redirect('checkout')
        try:
            address = Address.objects.get(id=id)
        except:
            address=None

        countries = Country.objects.all()
        states = State.objects.all()
        cities = City.objects.all()

        context={
            'address':address,
            'countries': countries,
            'states': states,
            'cities': cities,
        }
        return render(request, "public/user/address.html", context)
    
    def delete(request, id):
        
        user_address = UserAddress.objects.filter(address_id=id).first()
        user_address.address_id.delete()
        return redirect('checkout')