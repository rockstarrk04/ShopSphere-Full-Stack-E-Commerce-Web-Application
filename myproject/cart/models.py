from django.db import models
from django.contrib.auth.models import User
from products.models import ProductModel


# Create your models here.
class CartModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_c = models.ForeignKey(ProductModel,on_delete=models.CASCADE) 
    product_count = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)