from django.shortcuts import render, redirect
from django.contrib import messages, auth
from accounts.models import Account
from accounts.validator import Validator
from cart.models import Cart, CartItem
from cart.views import cart_id
from user.models import Address, UserAddress, Country, State, City
from accounts.utils import send_otp
from accounts.otp import TOTPVerification
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from wallet.views import create_wallet
from order.models import Order
from wallet.models import Transaction


# Create your views here.
otp_verification = TOTPVerification()

def verification_required(function):
  """
  Decorator for views that checks if a user is verified.

  If the user is not verified, it redirects them to the verification page.
  """
  def wrapper(request, *args, **kwargs):
    if not request.user.is_verified:
      return redirect(reverse('verification'))
    return function(request, *args, **kwargs)
  return wrapper

def send(request):
    user = request.user
    otp = otp_verification.generate_token()
    send_otp(user.email, otp)
    messages.success(request, "Verification code sent to your email address.")
    return True

def account(request):

    if request.method=='POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        currentpassword = request.POST.get('currentpassword')
        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')

        user = Account.objects.get(username__exact=request.user.username)
        success=user.check_password(currentpassword)

        if success:
            if firstname:
                if Validator.validate_name(firstname):
                    messages.error(request, 'Please enter a valid first name.')
                else:
                    user.first_name = firstname
            if lastname:
                if Validator.validate_name(lastname):
                    messages.error(request, 'Please enter a valid last name.')
                else:
                    user.last_name = lastname
            if newpassword:
                if newpassword != confirmpassword:
                    messages.error(request, "The passwords provided do not match!")
                elif Validator.validate_password(newpassword):
                    messages.error(request, 'The password must contain at least 8 characters, including at least one letter, one digit, and one special character (@$!%*?&).')
                else:
                    user.set_password(newpassword)
                    messages.success(request, "Password has been updated!")
            user.save()
        else:
            messages.error(request, "Invalid credentials!")
        return redirect('account')

    address = UserAddress.objects.filter(user_id=request.user)
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    context={
        'addresses':address,
        'orders':orders,
        'transactions':transactions
    }
    return render(request, 'public/user/account.html', context)

def password(request):
    return render(request, 'public/user/password.html')

def signin(request):

    if request.user.id:
        user = request.user
        if not user.is_verified:
            return redirect('verification')
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
            return redirect('home')
            
        messages.error(request, 'Invalid credentials')
        return redirect('signin')
        
    return render(request, 'public/user/login.html')

def register(request):
    # Check if user is already logged in and verified
    if request.user.id:
        user = request.user
        if not user.is_verified:
            return redirect('verification')
        return redirect('home')

    # Handle POST request for user registration
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        username = email.split('@')[0].lower()

        # Validate form input
        if password != confirm_password:
            messages.error(request, "The passwords provided do not match!")
        elif Validator.validate_name(first_name):
            messages.error(request, 'Please enter a valid first name.')
        elif Validator.validate_name(last_name):
            messages.error(request, 'Please enter a valid last name.')
        elif Validator.validate_email(email):
            messages.error(request, 'Please enter a valid email address.')
        elif Validator.validate_password(password):
            messages.error(request, 'The password must contain at least 8 characters, including at least one letter, one digit, and one special character (@$!%*?&).')
        else:
            # Attempt to create user
            try:
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                messages.success(request, "User has been successfully created!")
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
                    create_wallet(user)
                otp = otp_verification.generate_token()
                send_otp(email, otp)  # Send OTP to the user's email
                messages.success(request, "Verification code sent to your email address.")
                return redirect('verification')
            except IntegrityError:
                messages.error(request, 'User already exists!')

    return render(request, 'public/user/register.html')

def signout(request):
    auth.logout(request)
    request.session.clear()
    return redirect('signin')

@login_required(login_url='signin')
def verification(request):
    
    user = request.user
    if not user.is_verified:
        if request.method == 'POST':
            otp_secret = request.POST['otp']
            
            if otp_verification.verify_token(otp_secret):
                try:
                    user = Account.objects.get(email=user.email)
                  
                    user.is_verified = True
                    user.save()
                    # Update only is_verified in session (optional)
                    user.is_verified = True
                    # Update only relevant field
                    return redirect('signin')
                except Account.DoesNotExist:
                    
                    messages.error(request, 'User not found!')
            else:
                messages.error(request, 'Invalid OTP')

            
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
            usr_addr = UserAddress.objects.filter(user_id=user).first()
            status =False
            if not usr_addr:
                status=True
            user_address = UserAddress.objects.create(user_id=user, address_id=address_instance, is_default=status)
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