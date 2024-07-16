from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from category.models import Category
from accounts.validator import Validator
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from core.models import image_upload_path
from django.conf import settings
from django.core.paginator import Paginator
import os

# Create your views here.
class Categories:

    @login_required(login_url='root_signin')
    def category(request):
        search = request.GET.get('search')
        if search:
            categories = Category.objects.filter(name__icontains=search)
        else:
            categories = Category.objects.all()
        items_per_page = 10
        paginator = Paginator(categories, items_per_page)
        page = request.GET.get('page')
        obj = paginator.get_page(page)
        admin = request.user
        context = {
            'admin':admin,
            'categories':obj
        }
        return render(request, 'public/admin/category.html', context)

    @login_required(login_url='root_signin')
    def add(request):
       
        if request.method == 'POST':

            if 'image' in request.FILES:

                image = request.FILES['image']


                if image and isinstance(image, InMemoryUploadedFile):
                    image_path = image_upload_path(None, image.name, 'categories')
                    absolute_image_path = os.path.join(settings.MEDIA_ROOT, image_path)


                    with open(absolute_image_path, 'wb') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)

            name = request.POST['name']
            description = request.POST['description']

            slug = name.lower().replace(" ","_")
        

            if (Validator.validate_data(name)):
                messages.error(request, 'Please enter a valid name.')
            else:
                Category.objects.create(name=name, description=description, slug=slug, image=image_path)
                messages.success(request, "Category has been successfully created.!")
                return redirect('root_categories')
        admin = request.user
        context = {
            'admin':admin,
        }
        return render(request, 'public/admin/add_category.html', context)

    @login_required(login_url='root_signin')
    def edit(request, id):
        
        if request.method == 'POST':
            # Fetch the product object
            category = Category.objects.get(id=id)

            # Handle images
            if 'image' in request.FILES:

                image = request.FILES['image']

                if image and isinstance(image, InMemoryUploadedFile):
                    image_path = image_upload_path(None, image.name, 'categories')
                    absolute_image_path = os.path.join(settings.MEDIA_ROOT, image_path)


                    with open(absolute_image_path, 'wb') as destination:
                        for chunk in image.chunks():
                            
                            destination.write(chunk)
                            category.image = image_path

            # Handle other form fields
            name = request.POST.get('name')
            description = request.POST.get('description')
            is_available = bool(request.POST.get('isAvailable'))  # Convert to boolean



            # Update product fields
            category.name = name
            category.description = description
            category.is_available = is_available
            category.save()
            return redirect('root_categories')

        # Fetch product and categories for rendering form
        category = Category.objects.get(id=id)
        admin = request.user
        context = {
            'admin':admin,
            'category': category
        }
        
        return render(request, 'public/admin/edit_category.html', context)
    

    @login_required(login_url='root_signin')
    def delete(request, id):
        
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('root_categories')
    

