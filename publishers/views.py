from django.shortcuts import render, redirect
from login.models import *

# Create your views here.


def index(request):
    if User.objects.filter(ip=request.META['REMOTE_ADDR']):
        return render(request, 'publishers.html')
    else:
        return redirect("../")