from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.db import connection

# Create your views here.


def login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		print(username, password)
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
