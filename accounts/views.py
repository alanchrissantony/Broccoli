from django.shortcuts import render, redirect
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
from django.db.models import Sum, Count, F



# Create your views here.

@login_required(login_url='root_signin')
def root(request):
    orders = Order.objects.all().order_by('-created_at')
    products = OrderProduct.objects.all().select_related('product__category').order_by('-created_at')

    # Initialize dictionaries with defaultdict
    dp = defaultdict(decimal.Decimal)
    product_obj = {}
    order_obj = {}
    count = defaultdict(int)
    sales = 0
    revenue = 0

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
    total = sum(values)


    context = {
        'orders': orders,
        'sales': sales,
        'revenue': round(revenue),
        'order_category': dp,
        'order_products': product_obj,
        'keys': keys,
        'values': values,
        'order_obj':order_obj,
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

            name = request.POST['name'].strip(' ')
            price = request.POST['price'].strip(' ')
            try:
                category = Category.objects.get(name=request.POST['category'])
            except Category.DoesNotExist:
                messages.error(request, 'Please select a valid category.')
                return redirect('root/products/add')
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
                    return redirect('/root/products/edit/{{id}}')
                
        
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

    
class Orders:
    @login_required(login_url='root_signin')
    def orders(request):
        order = Order.objects.all()
        items_per_page = 10
        paginator = Paginator(order, items_per_page)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

        context={
            'orders':obj
        }
        return render(request, 'public/admin/orders.html', context)
    
    @login_required(login_url='root_signin')
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
    
    def delete(request, id):
        try:
            order = Order.objects.get(id=id)
            products = OrderProduct.objects.filter(order=order)
            for product in products:
                
                product.product.stock += product.quantity
                product.product.save()
            print(order)
            order.delete()
        except:
            pass
        return redirect('root_orders')


    def cancellation(request):
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

    def user_wallet(request):
        wallet = Wallet.objects.all()
        items_per_page = 10
        paginator = Paginator(wallet, items_per_page)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

        context={
            'wallets':obj
        }
        return render(request, 'public/admin/wallets.html', context)
    

    def view(request, id, wallet=None):
        user = Wallet.objects.filter(id=id).first()
        
        if user:
            wallet = Transaction.objects.filter(user=user.user).order_by('-created_at')
            user=user.user
        print(wallet, id)
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

        def product_discount(request):
            Discount.auto_delete_expired()
            discounts = Discount.objects.filter()
            items_per_page = 10
            paginator = Paginator(discounts, items_per_page)
            page = request.GET.get('page')
            obj = paginator.get_page(page)
            context = {
                'discounts':obj
                }
            return render(request, 'public/admin/discounts.html', context)
        
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
        
        def product_coupon(request):
            Coupon.auto_delete_expired()
            coupons = Coupon.objects.all()
            items_per_page = 10
            paginator = Paginator(coupons, items_per_page)
            page = request.GET.get('page')
            obj = paginator.get_page(page)
            context = {
                'coupons':obj
                }
            return render(request, 'public/admin/coupons.html', context)
        
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
        
        def product_promotion(request):
            promotions = Promotion.objects.all()
            items_per_page = 10
            paginator = Paginator(promotions, items_per_page)
            page = request.GET.get('page')
            obj = paginator.get_page(page)
            context = {
                'promotions':obj
                }
            return render(request, 'public/admin/product_promotions.html', context)
        
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
        
        def category_promotion(request):
            promotions = PromotionCategory.objects.all()
            items_per_page = 10
            paginator = Paginator(promotions, items_per_page)
            page = request.GET.get('page')
            obj = paginator.get_page(page)
            context = {
                'promotions':obj
                }
            return render(request, 'public/admin/category_promotions.html', context)
        
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
