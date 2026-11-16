from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name = 'home'),
    path('about/',about,name = 'about'),
    path('view_product/<int:pk>',view_product,name = 'view_product')
]