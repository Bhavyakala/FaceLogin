from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import NewUserForm, NewAuthenticationForm
from django.contrib.auth import  login,logout
from .backends import FaceAuthBackend
import base64

def homepage(request) :
    return render(request=request, template_name="main/home.html")

def register(request):
    if request.method=='POST':
        form = NewUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.description = form.cleaned_data.get('description')
            user.profile.picture = form.cleaned_data.get('picture')
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            messages.info(request, f"You are logged in as {username}")
            return render(request, "main/profile.html", context={'profile': user.profile})
        else:
            print(form.errors)
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
                print(form.error_messages[msg])
    
    form = NewUserForm()
    return render(request, "main/register.html", context = {'form': form})

def logout_request(request) :
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect("faceVerify:home")

def login_request(request, backend='faceVerify.backends.FaceAuthBackend') :
    if request.method == 'POST':
        form = NewAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            image = form.cleaned_data.get('image')
            print(type(image))
            f = FaceAuthBackend()
            user = f.authenticate(request, username, password)
            if user is not None:
                login(request,user)
                messages.info(request, f"You are logged in as {username}")
                return render(request, "main/profile.html", context={'profile': user.profile})
            else :
                messages.error(request, "Authentication Failed")
        else:
            print(form.errors)
            for msg in form.error_messages:
                messages.error(request, f"{form.error_messages[msg]}")
    form = NewAuthenticationForm()
    return render(request,"main/login.html", context={'form':form})
