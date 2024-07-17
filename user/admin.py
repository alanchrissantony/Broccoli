from django.contrib import admin
from user.models import Country, State, City, Address, UserAddress, Avatar
import cloudinary.uploader
from core.models import image_upload_path
from django import forms

# Register your models here.
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(UserAddress)


class AvatarAdminForm(forms.ModelForm):
    class Meta:
        model = Avatar
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

class AvatarAdmin(admin.ModelAdmin):
    form = AvatarAdminForm
    list_display = ('id', 'image')
    search_fields = ('id',)

admin.site.register(Avatar, AvatarAdmin)