from django.shortcuts import render, redirect
from login.models import User as user
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
# Create your views here.


def index(request):
    if user.objects.filter(status=1):
        return render(request, 'users.html')
    else:
        return redirect("../")