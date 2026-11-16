from django.shortcuts import render,get_object_or_404
from products.models import *
from django.contrib.auth.decorators import login_required
from authen.views import profile_img
from django.contrib import messages
# Create your views here.

def home(request):
    trend_msg=False
    no_product = False
    if request.user.is_authenticated:
        profile = profile_img(request)
    else:
        profile = False
    if 'category' in request.GET:
        cat = request.GET['category']
        category = CategoryModel.objects.get(cname = cat)
        all_products = ProductModel.objects.filter(is_delete = False , is_available = True,category_id = category).order_by('?')
    elif 'trend' in request.GET:
        all_products = ProductModel.objects.filter(is_delete = False , is_available = True,trending = True).order_by('?')
        if all_products.count()==0:
            trend_msg =True
            no_product = True
    elif 'offer' in request.GET:
        all_products = ProductModel.objects.filter(is_delete = False , is_available = True,offer = True).order_by('?')
        if all_products.count()==0:
            messages.error(request,'there is no offer available')
    else:   
        all_products = ProductModel.objects.filter(is_delete = False , is_available = True).order_by('?')
    category = []
    for i in CategoryModel.objects.all():
        if i.cname not in category:
            category.append(i.cname)
    return render(request,'home.html',{'products' : all_products,
                                       'category':category,'profile':profile,
                                       'trend_msg':trend_msg,'no_product':no_product})

@login_required(login_url='login_')
def about(request):
    if request.user.is_authenticated:
            profile = profile_img(request)
    else:
            profile = False
    return render(request,'about.html',{'profile':profile})

def view_product(request,pk):
    if request.user.is_authenticated:
        profile = profile_img(request)
    else:
        profile = False
    product = get_object_or_404(ProductModel,is_delete = False,is_available=True,id = pk)
    related_products = ProductModel.objects.filter(category = product.category).exclude(id=pk).order_by('?')[:3]
    return render(request,'view_product.html',{'product':product,'related_products':related_products,'profile':profile})