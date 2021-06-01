from django.shortcuts import render, redirect
from login.models import User

# Create your views here.


def index(request):
    href = 'home/' if User.objects.filter(status=1) else 'accounts/login'
    return render(request, 'index.html', {"href": href})


def home(request):
    if User.objects.filter(status=1):
        return render(request, 'home.html')
    else:
        return redirect("../")