from django.urls import path
from .views import *

urlpatterns = [
    path('login_/',login_,name='login_'),
    path('logout/',logout_,name='logout'),
    path('register/',register,name='register'),
    path('profile/',profile,name='profile'),
    path('pupdate/',update,name='pupdate'),
    path('reset_password/',reset_password,name='reset_password'),
    path('forgot_password/',forgot_password,name='forgot_password'),

]