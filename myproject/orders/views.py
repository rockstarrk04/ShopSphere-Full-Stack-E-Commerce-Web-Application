from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Prefetch
from .forms import AddressForm
from .models import AddressModel, OrderItem, Orders
from cart.models import CartModel


# Create your views here.

@login_required(login_url='login_')
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('check_out')
    else:
        form = AddressForm()
    return render(request,'add_address.html',{'form':form})

@login_required(login_url='login_')
def address(request):
    addresses = AddressModel.objects.filter(user = request.user)
    
    return render(request,'address.html',{'addresses':addresses})


@login_required(login_url='login_')
def order_(request):
    orders = Orders.objects.filter(user=request.user).select_related('address').prefetch_related(
        Prefetch('items', queryset=OrderItem.objects.select_related('product'))
    )
    return render(request, 'order_.html', {'orders': orders})

@login_required(login_url='login_')
def update_address(request,pk):
    data = get_object_or_404(AddressModel, id=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('address')
    form = AddressForm(instance=data)
    return render(request,'update_address.html',{'form':form})

@login_required(login_url='login_')
def remove_add(request,pk):
    get_object_or_404(AddressModel, id=pk, user=request.user).delete()
    return redirect('address')

@login_required(login_url='login_')
def check_out(request):
    address_list = AddressModel.objects.filter(user=request.user)
    cart_item = CartModel.objects.filter(user=request.user).select_related('product_c')

    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = get_object_or_404(AddressModel, id=address_id, user=request.user)
        if not cart_item.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('cart')

        with transaction.atomic():
            cart_item = list(
                CartModel.objects.select_related('product_c').filter(user=request.user)
            )
            for item in cart_item:
                if (
                    not item.product_c.is_available
                    or item.product_c.is_delete
                    or item.product_count > item.product_c.quantity
                ):
                    messages.error(
                        request,
                        f'Not enough stock is available for {item.product_c.pname}.',
                    )
                    return redirect('cart')

            grand_total = sum(
                (item.total_price for item in cart_item),
                start=Decimal('0.00'),
            )
            order = Orders.objects.create(
                user=request.user,
                address=address,
                total_amount=grand_total,
            )
            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=item.product_c,
                    price=item.product_c.price,
                    quantity=item.product_count,
                )
                for item in cart_item
            ])
            for item in cart_item:
                product = item.product_c
                product.quantity -= item.product_count
                if product.quantity == 0:
                    product.is_available = False
                product.save(update_fields=['quantity', 'is_available'])
            CartModel.objects.filter(user=request.user).delete()

        messages.success(request, f'Order #{order.id} placed successfully.')
        return redirect('order_')

    grand_total = sum(
        (i.total_price for i in cart_item),
        start=Decimal('0.00'),
    )
    context = {
        'address_list':address_list,
        'cart_item':cart_item,
        'grand_total':grand_total

    }
    return render(request,'check_out.html',context)