from django.shortcuts import render
from product.models import Product
from category.models import Category
from django.http import JsonResponse
from django.core.paginator import Paginator
from order.models import Review

# View-Level Caching
def product(request):
    items_per_page = 9
    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    category = request.GET.get('category')


    if search:
        products = Product.objects.filter(name__icontains=search, is_available=True)
    elif category and sort_by:
        products = Product.objects.filter(category=category, is_available=True).order_by(sort_by)
    elif sort_by:
        products = Product.objects.filter(is_available=True).order_by(sort_by)
    elif category:
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.all().exclude(is_available=False)

    paginator = Paginator(products, items_per_page)
    page = request.GET.get('page')
    products = paginator.get_page(page)


    top_rated = Product.objects.all().exclude(is_available=False).order_by('-rating')[:5]
    categories = Category.objects.all().exclude(is_available=False)

    context = {
        'products': products,
        'categories': categories,
        'top_rated': top_rated,
        'sort_by': sort_by,
        'search': search,
        'category': category,
    }
    return render(request, 'public/user/products.html', context)


def productDetails(request, id):
    if request.method == 'POST':
        response_data = {'message': 'Product added to cart successfully!'}
        return JsonResponse(response_data)


    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)
    top_rated = Product.objects.all().exclude(is_available=False).order_by('-rating')[:5]
    reviews = Review.objects.filter(product=product)

    context = {
        'product': product,
        'related_products': related_products,
        'top_rated': top_rated,
        'reviews': reviews,
        'review_count': len(reviews)
    }
    return render(request, 'public/user/product-details.html', context)