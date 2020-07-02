from django.shortcuts import render, redirect

from .forms import NewUserForm

def homepage(request) :
    return render(request=request, template_name="main/home.html",)