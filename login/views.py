from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.db import connection

# Create your views here.


def login(request):
	return render(request, 'login.html')

