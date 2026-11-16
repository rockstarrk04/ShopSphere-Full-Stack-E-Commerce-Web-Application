from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from authen.views import profile_img
from products.models import ProductModel
from .models import CartModel

# Create your views here.
@login_required(login_url='login_')
def add_to_cart(request,pk):
    item = get_object_or_404(ProductModel, id=pk, is_delete=False, is_available=True)
    try:
        cart_item = CartModel.objects.get(user=request.user, product_c=item)
        if cart_item.product_count >= item.quantity:
            messages.error(request, 'There is not enough stock for this product.')
            return redirect('cart')
        cart_item.product_count += 1 
        cart_item.total_price += item.price
        cart_item.save()
        return redirect('cart')
    except CartModel.DoesNotExist:
        if item.quantity < 1:
            messages.error(request, 'This product is out of stock.')
            return redirect('home')
        CartModel.objects.create(
            user = request.user,
            product_c = item,
            total_price = item.price
        )
    return redirect('home')

@login_required(login_url='login_')
def cart(request):
    profile = profile_img(request)
    cart_item = CartModel.objects.filter(user=request.user)
    TA = Decimal('0.00')
    for i in cart_item:
        TA+=i.total_price
    return render(request,'cart.html',{'profile':profile,'cart_item':cart_item,'TA':TA})

@login_required(login_url='login_')
def remove(request,pk):
    get_object_or_404(CartModel, id=pk, user=request.user).delete()
    return redirect('cart')

@login_required(login_url='login_')
def plus(request,pk):
    data = get_object_or_404(CartModel, id=pk, user=request.user)
    if data.product_count >= data.product_c.quantity:
        messages.error(request, 'There is not enough stock for this product.')
        return redirect('cart')
    data.product_count +=1
    data.total_price += data.product_c.price
    data.save()
    return redirect('cart')

@login_required(login_url='login_')
def minus(request,pk):
    data = get_object_or_404(CartModel, id=pk, user=request.user)
    if data.product_count  >1:
        data.product_count -=1
        data.total_price -= data.product_c.price
        data.save()
    else:
        data.delete()
    return redirect('cart')