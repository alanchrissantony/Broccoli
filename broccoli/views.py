# Create your views here.
from django.shortcuts import render

def error_404(request, exception):
        return render(request, 'public/user/404.html', {})