from layout.models import Slide, Banner
import cloudinary.uploader
from django.shortcuts import render
from core.models import image_upload_path

# Create your views here.

def layout(request):

    if request.method == 'POST':

        if 'slide_1' in request.FILES:

            slide_1=request.FILES['slide_1']
            slide = Slide.objects.filter().first()

            image_path=image_upload_path()
            cloudinary.uploader.upload(slide_1, public_id=image_path)
            

            if slide:
                slide.image=image_path
            else:
                slide = Slide.objects.create(image=image_path) 
            slide.save()
        
        if 'slide_2' in request.FILES:

            slide_2=request.FILES['slide_2']
            slide = Slide.objects.filter()

            image_path=image_upload_path()
            cloudinary.uploader.upload(slide_2, public_id=image_path)

            if len(slide)>1:
                slide=slide.last()
                slide.image=image_path
            else:
                slide = Slide.objects.create(image=image_path) 
            slide.save()
        
        if 'banner' in request.FILES:

            banner=request.FILES['banner']
            crnt_banner = Banner.objects.filter().first()

            image_path=image_upload_path()
            cloudinary.uploader.upload(banner, public_id=image_path)

            if crnt_banner:
                crnt_banner.image=image_path
            else:
                crnt_banner = Banner.objects.create(image=image_path) 
            crnt_banner.save()

    slides = Slide.objects.all()
    banner = Banner.objects.all()
    context = {
        'banner':banner,
        'slides':slides
    }
    return render(request, 'public/admin/layouts.html', context)