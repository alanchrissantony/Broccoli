from django import forms
from django.contrib import admin
from .models import Category
import cloudinary.uploader
from core.models import image_upload_path

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        image = self.cleaned_data.get('image')

        if image:
            filename = image_upload_path()
            cloudinary.uploader.upload(image, public_id=filename)
            instance.image = filename

        if commit:
            instance.save()
        return instance

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('name', 'slug', 'description', 'is_available', 'created_at', 'modified_at')
    search_fields = ('name', 'slug')

admin.site.register(Category, CategoryAdmin)