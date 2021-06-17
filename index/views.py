from django.shortcuts import render, redirect
from login.models import User
from users.models import User as Customer
from books.models import Books
from orders.models import Orders
from django.utils import timezone

# Create your views here.


def index(request):
    href = 'home/' if User.objects.filter(ip=request.META['REMOTE_ADDR']) else 'accounts/login'
    print(request.META['REMOTE_ADDR'])
    return render(request, 'index.html', {"href": href})


def home(request):
    if User.objects.filter(ip=request.META['REMOTE_ADDR']):
        if request.method == "GET":
            pass
        return render(request, 'home.html')
    else:
        return redirect("../")