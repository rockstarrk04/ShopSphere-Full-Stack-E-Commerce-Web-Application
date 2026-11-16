from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CategoryModel)
class CategoryModel(admin.ModelAdmin):
    model = CategoryModel
    list_display = ['id','cname','image','is_delete','createdat']
    search_fields = ['cname']


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    model = ProductModel
    list_display = ['id','pname','price','pimage','pdesc','is_available','is_delete',
                    'quantity','category','created_at']
    search_fields = ['pname']
    

