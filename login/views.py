from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db import connection
from .forms import *

# Create your views here.


def login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = User.objects.filter(username=username, pwd=password)
		email = User.objects.filter(email=username, pwd=password)
		if user:
			return HttpResponse(user)
		elif email:
			return HttpResponse(list(email)[0].pwd)
		else:
			return render(request, 'login.html', {'errmsg': 'Username or password error'})
	return render(request, 'login.html')


def signup(request):
	if request.method == "POST":
		username = request.POST.get('username')
		name = request.POST.get('name')
		password = request.POST.get('password')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		address = request.POST.get('address 1')
		print(username, name, password, email, phone, address)
	return render(request, 'signup.html')
