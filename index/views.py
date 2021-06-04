from django.shortcuts import render, redirect
from login.models import User

# Create your views here.


def index(request):
    href = 'home/' if User.objects.filter(ip=request.META['REMOTE_ADDR']) else 'accounts/login'
    print(request.META['REMOTE_ADDR'])
    return render(request, 'index.html', {"href": href})


def home(request):
    if User.objects.filter(ip=request.META['REMOTE_ADDR']):
        return render(request, 'home.html')
    else:
        return redirect("../")