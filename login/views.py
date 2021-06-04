from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.db import connection
from .forms import *

# Create your views here.


def login(request):
	User.objects.filter(ip=request.META['REMOTE_ADDR']).update(ip=False)
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = User.objects.filter(username=username)
		email = User.objects.filter(email=username)
		if user:
			if User.objects.get(username=username).pwd == password:
				User.objects.filter(username=username).update(ip=request.META['REMOTE_ADDR'])
				return redirect('../../home/')
			else:
				return render(request, 'login.html', {'errmsg2': 'Password error', 'username': username})
		elif email:
			if User.objects.get(email=username).pwd == password:
				User.objects.filter(email=username).update(ip=request.META['REMOTE_ADDR'])
				return redirect('../../home/')
			else:
				return render(request, 'login.html', {'errmsg2': 'Password error', 'username': email.first().email})
		else:
			return render(request, 'login.html', {'errmsg1': 'No such Username or Email'})
	return render(request, 'login.html')


def signup(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		email = request.POST.get('email')
		if User.objects.filter(username=username):
			return render(request, 'signup.html', {'errmsg1': 'Username used', 'email': email, 'password1': password1,
												'password2': password2})
		if User.objects.filter(email=email):
			return render(request, 'signup.html', {'errmsg2': 'Email used', 'username': username, 'password1': password1,
												'password2': password2})
		if password1 != password2:
			return render(request, 'signup.html', {'errmsg3': 'Please input the same password', 'username': username,
												'email': email, 'password1': password1})
		newuser = User.objects.create(username=username, email=email, pwd=password1)
		return redirect('../login')
	return render(request, 'signup.html')


def logout(request):
	User.objects.filter(ip=request.META['REMOTE_ADDR']).update(ip=0)
	return redirect("../../")