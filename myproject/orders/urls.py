from django.urls import path
from .views import *


urlpatterns = [
    path('check_out/',check_out,name='check_out'),
    path('order_/',order_,name='order_'),
    path('add_address/',add_address,name='add_address'),
    path('address/',address,name='address'),
    path('update_address/<int:pk>',update_address,name='update_address'),
    path('remove_add/<int:pk>',remove_add,name='remove_add'),
]