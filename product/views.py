from django.shortcuts import render, redirect
from product.models import Product
from category.models import Category
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.
def product(request):
    items_per_page = 9
    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    category = request.GET.get('category')
    if search:
        products = Product.objects.filter(name__icontains=search)
    elif sort_by:
        products = Product.objects.all().order_by(sort_by)
    elif category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, items_per_page)

    page = request.GET.get('page')
    obj = paginator.get_page(page)

    top_rated = Product.objects.all().order_by('-rating')[:5]
    categories = Category.objects.all()
    context = {
        'products' : obj,
        'categories' : categories,
        'top_rated':top_rated
    }
    return render(request, 'public/user/products.html', context)

def productDetails(request, id):
    if request.method == 'POST':
        response_data = {'message': 'Product added to cart successfully!'}
        return JsonResponse(response_data)
    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    top_rated = Product.objects.all().order_by('-rating')[:5]

    context = {
        'product' : product,
        'related_products' : related_products,
        'top_rated':top_rated
    }
    return render(request, 'public/user/product-details.html', context)

