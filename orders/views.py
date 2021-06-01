from django.shortcuts import render, redirect
from login.models import *

# Create your views here.


def index(request):
    if User.objects.filter(status=1):
        return render(request, 'orders.html')
    else:
        return redirect("../")
