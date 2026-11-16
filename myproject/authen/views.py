from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PictureModel
from .forms import RegisterForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def login_(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            messages.success(request,'Login Successful!!')
            return redirect('home')
        
        else:
            messages.error(request,'Password or Username is incorrect please enter valid details ')
            return redirect('login_')
    
    return render(request,'login_.html')


@login_required(login_url='login_')
def logout_(request):
    logout(request)
    messages.success(request,"logout successful!!")
    return redirect('login_')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            PictureModel.objects.create(user = user)
            return redirect('login_')
    else:
        form = RegisterForm()
        
    return render(request,'register.html',{'form':form})


@login_required(login_url='login_')
def profile(request):
    data = PictureModel.objects.get_or_create(user=request.user)
    profile = profile_img(request)
    return render(request,'profile.html',{'data':data,'profile':profile})


def profile_img(request):
    return get_object_or_404(PictureModel,user=request.user) 

@login_required(login_url='login_')
def reset_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST) # Pass the logged-in user and submitted form data

        if form.is_valid():  # Check whether the old and new passwords are valid 
            user = form.save()  # Save the new password in the database
            update_session_auth_hash(request, user)  # Keep the user logged in after changing the password
            messages.success(request, "Password changed successfully.")
            return redirect("profile")
    else:
        form = PasswordChangeForm(user=request.user)  # Display an empty password change form

    return render(request, "reset_password.html", {"form": form})




@login_required(login_url='login_')
def update(request):
    img = profile_img(request)
    profile = PictureModel.objects.get(user = request.user)
    user =request.user
    
    
    data = {
        'data':user,
        'image':profile
    }

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pic = request.FILES.get('image')  
        
        profile.image = pic if pic else profile.image
        profile.save() 
        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        messages.success(request,'Updated Profile Successfully..!!')
        return redirect('profile')
    
    return render(request,'update.html',{"data" : data,'img':img})





def forgot_password(request):
    if request.method == 'POST':
        if 'username' in request.POST:
            username = request.POST.get('username')
            request.session['forgot_username'] = username
            if User.objects.filter(username=username).exists():
                return render(request, 'forgot_password.html', {'new': True})
            else:
                messages.error(request, 'Username is not valid')
                return render(request, 'forgot_password.html')

        elif 'password' in request.POST:
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('cpassword')
            username = request.session.get('forgot_username')

            if not username:
                messages.error(request, 'Session expired. Please start over.')
                return redirect('forgot_password')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return render(request, 'forgot_password.html', {'new': True})

            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Updated the password successfully!')
            return redirect('login_')

    return render(request, 'forgot_password.html')