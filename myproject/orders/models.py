from django.db import models
from django.contrib.auth.models import User
from products.models import ProductModel


# Create your models here.
class AddressModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    address_line = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Orders(models.Model):
    STATUS_CHOICES = (
        ('pending','pending'),
        ('confirmed','confirmed'),
        ('shipped','shipped'),
        ('delivered','delivered'),
        ('cancelled','cancelled')
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.ForeignKey(AddressModel,on_delete=models.SET_NULL,null=True,blank=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField()
