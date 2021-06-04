from django.shortcuts import render, redirect
from login.models import User

# Create your views here.


def index(request):
    if User.objects.filter(ip=request.META['REMOTE_ADDR']):
        return render(request, 'writers.html')
    else:
        return redirect("../")
