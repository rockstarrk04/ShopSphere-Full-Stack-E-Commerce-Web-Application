from django.db import models

# Create your models here.
class CategoryModel(models.Model):
    cname = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/',null=True,default='guts.jpg')
    is_delete = models.BooleanField(default = False)
    createdat = models.DateTimeField(auto_now_add = True)




class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    pname = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pdesc = models.CharField(max_length=100)
    quantity = models.IntegerField()
    pimage = models.ImageField(upload_to='products',default='guts.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    trending = models.BooleanField(default=False)
    offer = models.BooleanField(default=False)

