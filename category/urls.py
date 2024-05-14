from django.urls import path
from . import views

urlpatterns = [
    path('', views.Categories.category, name="root_categories"),
    path('add', views.Categories.add, name="root_add_categories"),
    path('edit/<int:id>', views.Categories.edit, name="root_edit_categories"),
    path('delete/<int:id>', views.Categories.delete, name="root_delete_categories"),
]