from django.shortcuts import render, redirect
from accounts.models import Account
from user.models import UserAddress
from order.models import OrderProduct, OrderStatus, Order
from django.contrib.auth.decorators import login_required
from product.models import Product, Image
from category.models import Category
from cart.models import CartItem
from accounts.validator import Validator
from django.contrib import messages, auth
from accounts.tests import JsonEncoder
from django.views.decorators.cache import cache_control
from core.models import image_upload_path
from django.conf import settings
from django.core.paginator import Paginator
import json, os



# Create your views here.

@login_required(login_url='root_signin')
def root(request, sales=0):
    orders = Order.objects.all().order_by('-created_at')
    for order in orders:
        sales+=order.price
    sales = round(sales)
    context={
        'orders':orders,
        'sales':sales
    }
    return render(request, 'public/admin/dashboard.html', context)


class Authentication:

    def signin(request):
        if 'admin' in request.session:
            return redirect('root')
        if request.method == 'POST':
            email = request.POST["email"]
            password = request.POST["password"]
            
            admin = auth.authenticate(email=email, password=password)
            if admin and admin.is_admin:
                if admin.is_active:
                    auth.login(request, admin)
                    request.session['user']=json.dumps(admin, cls=JsonEncoder)
                    return redirect('root')
                messages.error(request, "Your account has been temporarily blocked!")
            else:
                messages.error(request, "Invalid credentials")
                
        return render(request, 'public/admin/signin.html')
    
    def signup(request):
        if 'admin' in request.session:
            return redirect('root')
        return render(request, 'public/admin/signup.html')
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def signout(request):
        auth.logout(request)
        request.session.clear()
        return redirect('root_signin')
    

class Products:

    @login_required(login_url='root_signin')
    def products(request):
        
        products = Product.objects.all()

        admin = request.user
        context = {
            'admin':admin,
            'products':products,
        }
        return render(request, 'public/admin/products.html', context)

    @login_required(login_url='root_signin')
    def add(request):
        
        if request.method == 'POST':
            images = request.FILES.getlist('image')  # Get list of uploaded images

            # Create a list to store the paths of uploaded images
            image_paths = []

            # Process each uploaded image
            for image in images:
                # Save the image to the media directory
                image_path = image_upload_path(None, image.name, 'products')
                absolute_image_path = os.path.join(settings.MEDIA_ROOT, image_path)

                with open(absolute_image_path, 'wb') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                # Add the image path to the list
                image_paths.append(image_path)

            name = request.POST['name']
            price = request.POST['price']
            try:
                category = Category.objects.get(name=request.POST['category'])
            except Category.DoesNotExist:
                messages.error(request, 'Please select a valid category.')
                return redirect('root/products/add')
            stock = request.POST['stock']
            description = request.POST['description']
            slug = name.lower().replace(" ", "_")

            if Validator.validate_data(name):
                messages.error(request, 'Please enter a valid name.')
            elif Validator.validate_data(stock):
                messages.error(request, 'Please enter a valid stock.')
            else:
                # Create the product object
                product = Product.objects.create(
                    name=name,
                    category=category,
                    price=price,
                    stock=stock,
                    description=description,
                    slug=slug
                )
                # Associate uploaded images with the product
                for image_path in image_paths:
                    img = Image.objects.create(image=image_path)
                    product.images.add(img)

                messages.success(request, "Product has been successfully added!")
                return redirect('root_products')

        # If the request method is not POST, render the add product form
        categories = Category.objects.all()
        admin = request.user
        context = {
            'admin':admin,
            'categories': categories
        }
        return render(request, 'public/admin/add_product.html', context)
    

    @login_required(login_url='root_signin')
    def edit(request, id):

        if request.method == 'POST':
            # Fetch the product object
            product = Product.objects.get(id=id)

            # Handle images
            images = request.FILES.getlist('image')  # Get list of uploaded images
            for image in images:
                # Create a new Image object for each uploaded image
                img = Image.objects.create(image=image)
                # Add the image to the product's images
                product.images.add(img)

            # Handle other form fields
            name = request.POST.get('name')
            price = request.POST.get('price')
            category_name = request.POST.get('category')
            category = Category.objects.get(name=category_name)
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            is_available = bool(request.POST.get('isAvailable'))  # Convert to boolean

                # Update product fields
            product.name = name
            product.price = price
            product.category = category
            product.stock = stock
            product.description = description
            product.is_available = is_available

            product.save()
            return redirect('root_products')

        # Fetch product and categories for rendering form
        product = Product.objects.get(id=id)
        categories = Category.objects.all()
        admin = request.user
        context = {
            'admin':admin,
            'product': product,
            'categories': categories
        }
        return render(request, 'public/admin/edit_product.html', context)
    
    @login_required(login_url='root_signin')
    def delete(request, id):
        
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('root_products')
    
    @login_required(login_url='root_signin')
    def delete_image(request, id):
        
        image = Image.objects.get(id=id)
        image.delete()
    
class Users:

    @login_required(login_url='root_signin')
    def users(request):
        users = Account.objects.all().filter(is_admin=False)
        admin = request.user
        context = {
            'admin':admin,
            'users':users
        }
        return render(request, 'public/admin/users.html', context)

    @login_required(login_url='root_signin')
    def add(request):
        
        if request.method == 'POST':

            first_name = request.POST.get('firstname').strip(' ')
            last_name = request.POST.get('lastname').strip(' ')
            email = request.POST.get('email').strip(' ')
            username = request.POST.get('username').strip(' ')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirmpassword')


            if password == confirm_password:
                if (Validator.validate_name(first_name)):
                    messages.error(request, 'Please enter a valid first name.')
                elif(Validator.validate_name(last_name)):
                    messages.error(request, 'Please enter a valid last name.')
                elif(Validator.validate_email(email)):
                    messages.error(request, 'Please enter a valid email address.')
                elif(Validator.validate_password(password)):
                    messages.error(request, 'The password must contain at least 8 characters, including at least one letter, one digit, and one special character (@$!%*?&).')
                else:
                    try:
                        user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                        messages.success(request, "User has been successfully created.!")
                    except:
                        messages.error(request, 'User already exists!')
            else:
                messages.error(request, "The passwords provided do not match!")
        return render(request, 'public/admin/add_user.html')

    @login_required(login_url='root_signin')
    def edit(request, id):

        
        if request.method == 'POST':

            is_active = request.POST.getlist('isActive')
            
            if is_active:
                is_active = False
            else:
                is_active =True

            user = Account.objects.get(id=id)

            user.is_active = is_active

            user.save()
            return redirect('root_users')

        try:
            user = Account.objects.get(id=id)
            address = UserAddress.objects.filter(user_id=user).first()
            if not user:
                raise ValueError

            admin = request.user
            context = {
                'admin':admin,
                'user':user,
                'address':address
                }
        except:
            return redirect('root_users')
        return render(request, 'public/admin/edit_user.html', context)
    

    @login_required(login_url='root_signin')
    def delete(request, id):
        
        user = Account.objects.get(id=id)
        user.delete()
        return redirect('/root/users')


class Carts:
    @login_required(login_url='root_signin')
    def carts(request):
        carts = CartItem.objects.all()
        context={
            'carts':carts
        }
        return render(request, 'public/admin/carts.html', context)
    
class Orders:
    @login_required(login_url='root_signin')
    def orders(request):
        items_per_page = 10
        order = OrderProduct.objects.all()

        paginator = Paginator(order, items_per_page)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

        context={
            'items':obj
        }
        return render(request, 'public/admin/orders.html', context)
    
    @login_required(login_url='root_signin')
    def edit(request, id):
        item = OrderProduct.objects.get(id=id)
        if request.method == "POST":
            status = request.POST['status']
            status, _ = OrderStatus.objects.get_or_create(name=status)
            item.order.statuses.add(status)
            return redirect("root_orders")

        statuses = OrderStatus.objects.all()
        context={
            'item':item,
            'statuses':statuses
        }
        return render(request, 'public/admin/edit_order.html', context)
    
    def delete(request, id):
        try:
            order = OrderProduct.objects.get(order=id)
            order.product.stock += order.quantity
            order.product.save()
            order.delete()
        except:
            pass
        return redirect('root_orders')
