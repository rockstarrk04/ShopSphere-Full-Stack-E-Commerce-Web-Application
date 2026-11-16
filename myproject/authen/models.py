from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PictureModel(models.Model):
    image = models.ImageField(upload_to='uploads/',default='guts.jpg',null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)