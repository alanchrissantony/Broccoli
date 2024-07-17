from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from accounts.models import Account
from user.models import UserAddress
from order.models import OrderProduct, OrderStatus, Order, OrderCancel
from django.contrib.auth.decorators import login_required
from product.models import Product, Image
from category.models import Category
from promotion.models import Discount, Promotion, PromotionCategory, Coupon
from accounts.validator import Validator
from django.contrib import messages, auth
from accounts.tests import JsonEncoder
from django.views.decorators.cache import cache_control
from core.models import image_upload_path
from django.conf import settings
from django.core.paginator import Paginator
from wallet.models import Wallet, Transaction
import json, os, uuid, decimal
from collections import defaultdict
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import Extract
from collections import defaultdict
import cloudinary.uploader
from cloudinary.utils import cloudinary_url


# Create your views here.
def chart(request):
    dx=[]
    dy=[]

    filter_by = request.GET.get('filter')
    current_date = datetime.now()
    current_year = datetime.now().year
    today = timezone.now().date()
    
    if filter_by == 'daily':
        for i in range(6):
            date = current_date - timedelta(days=i)
            dx.append(date.strftime("%a"))
        last_6_days = today - timedelta(days=6)
        orders = Order.objects.filter(
            created_at__gte=last_6_days,
            created_at__lt=today,
            is_ordered=True
        )
        day_counts = (
            orders.annotate(day=Extract('created_at', 'day'))
            .annotate(month=Extract('created_at', 'month'))
            .annotate(year=Extract('created_at', 'year'))
            .values('year', 'month', 'day')
            .annotate(count=Count('id'))
            .order_by('year', 'month', 'day')
        )

        all_days = [
            (today.year, today.month, day) if day <= today.day else (today.year, today.month - 1, day)
            for day in range(today.day - 5, today.day + 1)
        ]

        day_counts_dict = {(entry['year'], entry['month'], entry['day']): entry['count'] for entry in day_counts}
        for year, month, day in all_days:
            if (year, month, day) not in day_counts_dict:
                day_counts_dict[(year, month, day)] = 0
        
        final_counts = [
            {'year': year, 'month': month, 'day': day, 'count': day_counts_dict[(year, month, day)]}
            for year, month, day in sorted(day_counts_dict.keys())
        ]

        dy = [entry['count'] for entry in final_counts]

    elif filter_by == 'monthly':
        for i in range(6):
            date = current_date - relativedelta(months=i)
            dx.append(date.strftime("%b"))
        last_6_months = today - timedelta(days=30 * 6)
        orders = Order.objects.filter(
        created_at__gte=last_6_months,
        created_at__lt=today,
        is_ordered=True
    )
        month_counts = (
        orders.annotate(month=Extract('created_at', 'month'))
        .annotate(year=Extract('created_at', 'year'))
        .values('year', 'month')
        .annotate(count=Count('id'))
        .order_by('year', 'month')
    )
        all_months = [
        (today.year, month) if month <= today.month else (today.year - 1, month)
        for month in range(today.month - 5, today.month + 1)
    ]

        month_counts_dict = {(entry['year'], entry['month']): entry['count'] for entry in month_counts}
        for year, month in all_months:
            if (year, month) not in month_counts_dict:
                month_counts_dict[(year, month)] = 0

        final_counts = [
        {'year': year, 'month': month, 'count': month_counts_dict[(year, month)]}
        for year, month in sorted(month_counts_dict.keys())
    ]
        
        dy = [entry['count'] for entry in final_counts]
    else:
        dx=[current_year - i for i in range(6)]
        last_6_years = today - timedelta(days=365 * 6)
        orders = Order.objects.filter(
            created_at__gte=last_6_years,
            created_at__lt=today,
            is_ordered=True
        )
        year_counts = (
            orders.annotate(year=Extract('created_at', 'year'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )

        all_years = [
            today.year - i for i in range(6)
        ]

        year_counts_dict = {entry['year']: entry['count'] for entry in year_counts}
        for year in all_years:
            if year not in year_counts_dict:
                year_counts_dict[year] = 0

        final_counts = [
            {'year': year, 'count': year_counts_dict[year]}
            for year in sorted(year_counts_dict.keys())
        ]
        dy = [entry['count'] for entry in final_counts]

    dx.reverse()

    context={
        'dx':dx,
        'dy':dy,
    }
    return JsonResponse(context)

def superuser_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('root_signin'))
        elif not request.user.is_superuser:
            return redirect(reverse('root_signin'))
        return view_func(request, *args, **kwargs)
    return login_required(_wrapped_view_func)


@superuser_required
def root(request):
    orders = Order.objects.all().order_by('-created_at')
    products = OrderProduct.objects.all().select_related('product__category').order_by('-created_at')

    # Initialize dictionaries with defaultdict
    dp = defaultdict(decimal.Decimal)
    dx=[]
    dy=[]
    product_obj = {}
    order_obj = {}
    count = defaultdict(int)
    sales = 0
    revenue = 0

    current_year = datetime.now().year
    today = datetime.now().date()

    dx=[current_year - i for i in range(6)]
    last_6_years = today - timedelta(days=365 * 6)
    orders = Order.objects.filter(
        created_at__gte=last_6_years,
        created_at__lt=today,
        is_ordered=True
    )
    year_counts = (
        orders.annotate(year=Extract('created_at', 'year'))
        .values('year')
        .annotate(count=Count('id'))
        .order_by('year')
    )
    all_years = [
        today.year - i for i in range(6)
    ]
    year_counts_dict = {entry['year']: entry['count'] for entry in year_counts}
    for year in all_years:
        if year not in year_counts_dict:
            year_counts_dict[year] = 0
    final_counts = [
        {'year': year, 'count': year_counts_dict[year]}
        for year in sorted(year_counts_dict.keys())
    ]
    dy = [entry['count'] for entry in final_counts]
    dx.reverse()
    
    # Iterate through products and populate dictionaries
    for product in products:
        category = product.product.category
        dp[category] += product.price
        product_obj[category] = product.product.name
        count[category.name] += 1

    # Calculate total sales and revenue
    for order in orders:
        revenue += order.price
        sales += 1

        if(order.statuses.last() in order_obj):
            order_obj[order.statuses.last()]+=1
        else:
            order_obj[order.statuses.last()]=1

    

    # Convert count dictionary to keys and values lists
    keys = list(count.keys())
    values = list(count.values())
    
    context = {
        'orders': orders,
        'sales': sales,
        'revenue': round(revenue),
        'order_category': dp,
        'order_products': product_obj,
        'keys': keys,
        'values': values,
        'order_obj':order_obj,
        'dx':dx,
        'dy':dy
    }
    return render(request, 'public/admin/dashboard.html', context)


class Authentication:

    def signin(request):
        if request.user.is_superuser:
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
        if request.user.is_superuser:
            return redirect('root')
        return render(request, 'public/admin/signup.html')
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def signout(request):
        auth.logout(request)
        request.session.clear()
        return redirect('root_signin')
    

class Products:

    @superuser_required
    def products(request):
        search = request.GET.get('search')
        if search:
            products = Product.objects.filter(name__icontains=search)
        else:
            products = Product.objects.all()
        items_per_page = 10
        paginator = Paginator(products, items_per_page)
        page = request.GET.get('page')
        obj = paginator.get_page(page)
        admin = request.user
        context = {
            'admin':admin,
            'products':obj,
        }
        return render(request, 'public/admin/products.html', context)

    @superuser_required
    def add(request):
        
        if request.method == 'POST':
            images = request.FILES.getlist('image')  # Get list of uploaded images

            # Create a list to store the paths of uploaded images
            image_paths = []

            # Process each uploaded image
            for image in images:
                # Save the image to the media directory
                image_path = image_upload_path()
                cloudinary.uploader.upload(image, public_id=image_path)

                # Add the image path to the list
                image_paths.append(image_path)

            name = request.POST['name'].strip(' ')
            price = request.POST['price'].strip(' ')
            try:
                category = Category.objects.get(name=request.POST['category'])
            except Category.DoesNotExist:
                messages.error(request, 'Please select a valid category.')
                return redirect('account/products/add')
            stock = request.POST['stock'].strip(' ')
            description = request.POST['description'].strip(' ')
            slug = name.lower().replace(" ", "_")

            if Validator.validate_data(name):
                messages.error(request, 'Please enter a valid name.')
            elif Validator.validate_stock(stock):
                messages.error(request, 'Please enter a valid stock.')
            elif Validator.validate_price(price):
                messages.error(request, 'Please enter a valid price.')
            else:
                try:
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
                except:
                    messages.error(request, "Product already exists!")
                return redirect('root_products')

        # If the request method is not POST, render the add product form
        categories = Category.objects.all()
        admin = request.user
        context = {
            'admin':admin,
            'categories': categories
        }
        return render(request, 'public/admin/add_product.html', context)
    

    @superuser_required
    def edit(request, id):

        if request.method == 'POST':
            # Fetch the product object
            product = Product.objects.get(id=id)

            # Handle images
            images = request.FILES.getlist('image')  # Get list of uploaded images
            for image in images:

                image_path = image_upload_path()
                cloudinary.uploader.upload(image, public_id=image_path)
                # Create a new Image object for each uploaded image
                img = Image.objects.create(image=image_path)
                # Add the image to the product's images
                product.images.add(img)

            # Handle other form fields
            name = request.POST.get('name').strip(' ')
            price = request.POST.get('price').strip(' ')
            category_name = request.POST.get('category').strip(' ')
            stock = request.POST.get('stock').strip(' ')
            description = request.POST.get('description').strip(' ')
            is_available = bool(request.POST.get('isAvailable')) # Convert to boolean

            if Validator.validate_data(name):
                messages.error(request, 'Please enter a valid name.')
            elif Validator.validate_stock(stock) == True:
                messages.error(request, 'Please enter a valid stock.')
            elif Validator.validate_price(price) == True:
                messages.error(request, 'Please enter a valid price.')
            else:
                try:
                    category = Category.objects.get(name=category_name)

                    # Update product fields
                    product.name = name
                    product.price = price
                    product.category = category
                    product.stock = stock
                    product.description = description
                    product.is_available = is_available

                    product.save()
                except:
                    messages.error(request, 'Please select a valid category.')
                    return redirect(f'/accounts/products/edit/{id}')
                
        
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
    
    @superuser_required
    def delete(request, id):
        
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('root_products')
    
    @superuser_required
    def delete_image(request, id):
        
        image = Image.objects.get(id=id)
        image.delete()
    
class Users:

    @superuser_required
    def users(request):
        search = request.GET.get('search')
        if search:
            users = Account.objects.filter(username__icontains=search, is_admin=False)
        else:
            users = Account.objects.all().filter(is_admin=False)
        items_per_page = 10
        paginator = Paginator(users, items_per_page)
        page = request.GET.get('page')
        obj = paginator.get_page(page)
        admin = request.user
        context = {
            'admin':admin,
            'users':obj
        }
        return render(request, 'public/admin/users.html', context)

    @superuser_required
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

    @superuser_required
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
    

    @superuser_required
    def delete(request, id):
        
        user = Account.objects.get(id=id)
        user.delete()
        return redirect('/account/users')

    
class Orders:
    @superuser_required
    def orders(request):
        search = request.GET.get('search')
        if search:
            order = Order.objects.filter(user__username__icontains=search)
        else:
            order = Order.objects.all()
        items_per_page = 10
        paginator = Paginator(order, items_per_page)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

        context={
            'orders':obj
        }
        return render(request, 'public/admin/orders.html', context)
    
    @superuser_required
    def edit(request, id):
        order = Order.objects.get(id=id)
        products = OrderProduct.objects.filter(order=order)
        if request.method == "POST":
            status = request.POST['status']
            if status == 'Order Confirmed':
                status = 'Shipped'
            elif status == 'Shipped':
                status = 'Out for delivery'
            elif status == 'Out for delivery':
                status = 'Delivered'
            status, _ = OrderStatus.objects.get_or_create(name=status)
            order.statuses.add(status)
            return redirect("root_orders")

        context={
            'order':order,
            'products':products,
        }
        return render(request, 'public/admin/edit_order.html', context)
    
    @superuser_required
    def cancel(request, id):
        try:
            order = Order.objects.get(id=id)
            products = OrderProduct.objects.filter(order=order)
            if order.payment.status == 'Paid':
                wallet = Wallet.objects.filter(user=order.user).first()
                if wallet:
                    Transaction.objects.create(
                        transaction = uuid.uuid4(),
                        user = wallet.user,
                        amount = order.price,
                        balance = float(wallet.balance) + order.price,
                        status = 'Credit'
                    )
                    wallet.balance += decimal.Decimal(order.price)
                    wallet.save()
            cancel = OrderCancel.objects.create(order=order)
            
            for product in products:
                product.product.stock += product.quantity
                product.product.save()
            last_status = order.statuses.last().name
            if last_status == 'Order Confirmed':
                status, _ = OrderStatus.objects.get_or_create(name='Shipped')
                order.statuses.add(status)
                last_status = 'Shipped'
            
            if last_status == 'Shipped':
                status, _ = OrderStatus.objects.get_or_create(name='Out for delivery')
                order.statuses.add(status)
            status, _ = OrderStatus.objects.get_or_create(name='Cancelled')
            order.statuses.add(status)
            order.save()
    
        except:
            pass
        return redirect('root_orders')
    
    @superuser_required
    def delete(request, id):
        try:
            order = Order.objects.get(id=id)
            products = OrderProduct.objects.filter(order=order)
            for product in products:
                
                product.product.stock += product.quantity
                product.product.save()
      
            order.delete()
        except:
            pass
        return redirect('root_orders')


    def cancellation(request):
        search = request.GET.get('search')
        if search:
            orders = OrderCancel.objects.filter(order__user__username__icontains=search)
        else:
            orders = OrderCancel.objects.all().order_by('-created_at')
        items_per_page = 10
        paginator = Paginator(orders, items_per_page)
        page = request.GET.get('page')
        obj = paginator.get_page(page)
        context={
            'orders':obj
        }
        return render(request, 'public/admin/cancellation.html', context)
    

    

class UserWallet:
    @superuser_required
    def user_wallet(request):
        search = request.GET.get('search')
        if search:
            wallet = Wallet.objects.filter(user__username__icontains=search)
        else:
            wallet = Wallet.objects.all()
        items_per_page = 10
        paginator = Paginator(wallet, items_per_page)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

        context={
            'wallets':obj
        }
        return render(request, 'public/admin/wallets.html', context)
    
    @superuser_required
    def view(request, id, wallet=None):
        user = Wallet.objects.filter(id=id).first()
        
        if user:
            wallet = Transaction.objects.filter(user=user.user).order_by('-created_at')
            user=user.user
      
        items_per_page = 10
        paginator = Paginator(wallet, items_per_page)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

        context={
            'wallets':obj,
            'user':user
        }
        return render(request, 'public/admin/user_wallets.html', context)
    

class ProductPromotion:

    class ProductDiscount:

        @superuser_required
        def product_discount(request):
            Discount.auto_delete_expired()
            search = request.GET.get('search')
            if search:
                discounts = Discount.objects.filter(name__icontains=search)
            else:
                discounts = Discount.objects.filter()
            items_per_page = 10
            paginator = Paginator(discounts, items_per_page)
            page = request.GET.get('page')
            obj = paginator.get_page(page)
            context = {
                'discounts':obj
                }
            return render(request, 'public/admin/discounts.html', context)
        
        @superuser_required
        def add(request):
            if request.method == 'POST':
                name = request.POST.get('name').strip(' ')
                type = request.POST.get('type').strip(' ')
                discount = request.POST.get('discount').strip(' ')
                description = request.POST.get('description').strip(' ')
                start = request.POST.get('start').strip(' ')
                end = request.POST.get('end').strip(' ')

                try:
                    Discount.objects.create(
                        name = name,
                        type = type,
                        discount = discount,
                        description = description,
                        start_date = start,
                        end_date = end,
                    )
                    Discount.auto_delete_expired()
                    return redirect('root_discounts')
                except:   
                    messages.error(request, 'Unable to create discount!')
            context = {
                'types':Coupon.TYPE
            }
            return render(request, 'public/admin/add_discount.html', context)
        
        @superuser_required
        def edit(request, id):
            Discount.auto_delete_expired()
            discount = Discount.objects.filter(id=id).first()

            if request.method == 'POST':
                name = request.POST.get('name').strip(' ')
                status = request.POST.get('status')
                type = request.POST.get('type').strip(' ')
                _discount = request.POST.get('discount').strip(' ')
                description = request.POST.get('description').strip(' ')
                start = request.POST.get('start').strip(' ')
                end = request.POST.get('end').strip(' ')
        
                try:
                    discount.name = name
                    discount.type = type
                    discount.discount = _discount
                    discount.description = description
                    discount.start_date = start
                    discount.end_date = end
                    if status:
                        discount.status = True
                    else:
                        discount.status = False

                    discount.save()
                    Discount.auto_delete_expired()
                    return redirect('root_discounts')
                except:
                    messages.error(request, 'Unable to modify')
                    
            context = {
                'types':Coupon.TYPE,
                'discount':discount
                }
            return render(request, 'public/admin/edit_discount.html', context)
        
        @superuser_required
        def delete(request, id):
            discount = Discount.objects.filter(id=id).first()

            if discount.status:
                discount.status = False
            else:
                discount.status = True
            discount.save()
            Discount.auto_delete_expired()
            return redirect('root_discounts')
        

    class ProductCoupon:

        @superuser_required
        def product_coupon(request):
            Coupon.auto_delete_expired()
            search = request.GET.get('search')
            if search:
                coupons = Coupon.objects.filter(code__icontains=search)
            else:
                coupons = Coupon.objects.all()
            items_per_page = 10
            paginator = Paginator(coupons, items_per_page)
            page = request.GET.get('page')
            obj = paginator.get_page(page)
            context = {
                'coupons':obj
                }
            return render(request, 'public/admin/coupons.html', context)
        
        @superuser_required
        def add(request):
            if request.method == 'POST':
                code = request.POST.get('code').strip(' ')
                type = request.POST.get('type').strip(' ')
                discount = request.POST.get('discount').strip(' ')
                minimum_price = request.POST.get('minimum').strip(' ')
                maximum_redeem = request.POST.get('maximum').strip(' ')
                expiry = request.POST.get('end').strip(' ')

                try:
                    Coupon.objects.create(
                        code = code,
                        type = type,
                        discount = discount,
                        minimum_price = minimum_price,
                        maximum_redeem = maximum_redeem,
                        expiry = expiry,
                    )
                    Coupon.auto_delete_expired()
                    messages.success(request, 'Coupon has been successfully created!')
                    return redirect('root_coupons')
                except:   
                    messages.error(request, 'Unable to create coupon!')
            context = {
                'types':Coupon.TYPE
            }
            return render(request, 'public/admin/add_coupon.html', context)
        
        @superuser_required
        def edit(request, id):
            Coupon.auto_delete_expired()
            coupons = Coupon.objects.filter(id=id).first()

            if request.method == 'POST':
                code = request.POST.get('code').strip(' ')
                type = request.POST.get('type').strip(' ')
                discount = request.POST.get('discount').strip(' ')
                minimum_price = request.POST.get('minimum').strip(' ')
                maximum_redeem = request.POST.get('maximum').strip(' ')
                expiry = request.POST.get('end').strip(' ')
                status = request.POST.get('status')

                try:
                    coupons.code = code
                    coupons.type = type
                    coupons.discount = discount
                    coupons.minimum_price = minimum_price
                    coupons.maximum_redeem = maximum_redeem
                    coupons.expiry = expiry
                    if status:
                        coupons.status = True
                    else:
                        coupons.status = False

                    coupons.save()
                    Coupon.auto_delete_expired()
                    messages.success(request, 'Coupon has been successfully updated!')
                    return redirect('root_coupons')
                except:
                    messages.error(request, 'Unable to modify')

            context = {
                'coupons':coupons,
                'types':Coupon.TYPE
                }
            return render(request, 'public/admin/edit_coupon.html', context)
        
        @superuser_required
        def delete(request, id):
            coupon = Coupon.objects.filter(id=id).first()

            if coupon.status:
                coupon.status = False
            else:
                coupon.status = True
            coupon.save()
            Coupon.auto_delete_expired()
            messages.success(request, 'Coupon has been successfully deleted!')
            return redirect('root_coupons')
        
    
    class ProductPromotion:
        
        @superuser_required
        def product_promotion(request):
            search = request.GET.get('search')
            if search:
                promotions = Promotion.objects.filter(product__name__icontains=search)
            else:
                promotions = Promotion.objects.all()
            items_per_page = 10
            paginator = Paginator(promotions, items_per_page)
            page = request.GET.get('page')
            obj = paginator.get_page(page)
            context = {
                'promotions':obj
                }
            return render(request, 'public/admin/product_promotions.html', context)
        
        @superuser_required
        def add(request):
            products = Product.objects.filter(is_available=True)
            discounts = Discount.objects.filter(status=True)

            if request.method == 'POST':
                productId = request.POST.get('product')
                discountId = request.POST.get('discount')

                product = Product.objects.filter(id=productId).first()
                discount = Discount.objects.filter(id=discountId).first()

                try:
                    Promotion.objects.create(
                        product = product,
                        discount = discount
                    )
                    messages.success(request, 'Product promotion has been successfully created!')
                    return redirect('root_product_promotions')
                except:
                    messages.error(request, 'Unable to create product promotion!')

            context = {
                'products':products,
                'discounts':discounts
                }
            return render(request, 'public/admin/add_product_promotion.html', context)
        
        @superuser_required
        def edit(request, id):
            products = Product.objects.filter(is_available=True)
            discounts = Discount.objects.filter(status=True)
            promotion = Promotion.objects.filter(id=id).first()

            if request.method == 'POST':
                productId = request.POST.get('product')
                discountId = request.POST.get('discount')
                status = request.POST.get('status')

                product = Product.objects.filter(id=productId).first()
                discount = Discount.objects.filter(id=discountId).first()

                try:
                    promotion.product = product
                    promotion.discount = discount
                   
                    if status and discount.status:
                        promotion.status = True
                    else:
                        promotion.status = False
                    promotion.save()
                    messages.success(request, 'Product promotion has been successfully updated!')
                    return redirect('root_product_promotions')
                except:
                    messages.error(request, 'Unable to modify product promotion!')

            context = {
                'products':products,
                'discounts':discounts,
                'promotion':promotion
                }
            return render(request, 'public/admin/edit_product_promotion.html', context)
        
        @superuser_required
        def delete(request, id):
            promotion = Promotion.objects.filter(id=id).first()
            if promotion.discount.status:
                if promotion.status:
                    promotion.status = False
                else:
                    promotion.status = True
                promotion.save()
            messages.success(request, 'Promotion has been successfully deleted!')
            return redirect('root_product_promotions')



    class CategoryPromotion:
        
        @superuser_required
        def category_promotion(request):
            search = request.GET.get('search')
            if search:
                promotions = PromotionCategory.objects.filter(category__name__icontains=search)
            else:
                promotions = PromotionCategory.objects.all()
            items_per_page = 10
            paginator = Paginator(promotions, items_per_page)
            page = request.GET.get('page')
            obj = paginator.get_page(page)
            context = {
                'promotions':obj
                }
            return render(request, 'public/admin/category_promotions.html', context)
        
        @superuser_required
        def add(request):
            categories = Category.objects.filter(is_available=True)
            discounts = Discount.objects.filter(status=True)

            if request.method == 'POST':
                categoryId = request.POST.get('category')
                discountId = request.POST.get('discount')

                

                category = Category.objects.filter(id=categoryId).first()
                discount = Discount.objects.filter(id=discountId).first()
                
                try:
                    PromotionCategory.objects.create(
                        category = category,
                        discount = discount
                    )
                    messages.success(request, 'Category promotion has been successfully created!')
                    return redirect('root_category_promotions')
                except:
                    messages.error(request, 'Unable to create category promotion!')

            context = {
                'categories':categories,
                'discounts':discounts
                }
            return render(request, 'public/admin/add_category_promotion.html', context)
        
        @superuser_required
        def edit(request, id):
            categories = Category.objects.filter(is_available=True)
            discounts = Discount.objects.filter(status=True)
            promotion = PromotionCategory.objects.filter(id=id).first()

            if request.method == 'POST':
                categoryId = request.POST.get('category')
                discountId = request.POST.get('discount')
                status = request.POST.get('status')

                category = Category.objects.filter(id=categoryId).first()
                discount = Discount.objects.filter(id=discountId).first()

                try:
                    promotion.category = category
                    promotion.discount = discount
                  
                    if status and discount.status:
                        promotion.status = True
                    else:
                        promotion.status = False
                    promotion.save()
                    messages.success(request, 'Category promotion has been successfully updated!')
                    return redirect('root_category_promotions')
                except:
                    messages.error(request, 'Unable to modify category promotion!')

            context = {
                'categories':categories,
                'discounts':discounts,
                'promotion':promotion
                }
            return render(request, 'public/admin/edit_category_promotion.html', context)

        @superuser_required
        def delete(request, id):
            promotion = PromotionCategory.objects.filter(id=id).first()
            if promotion.discount.status:
                if promotion.status:
                    promotion.status = False
                else:
                    promotion.status = True
            promotion.save()
            messages.success(request, 'Promotion has been successfully deleted!')
            return redirect('root_category_promotions')
