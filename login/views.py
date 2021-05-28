from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.db import connection

# Create your views here.


def index(response, id):
	ls = User.object.get(id=id)
	return HttpResponse("<h1> %s </h1>" % ls.name)


def home(response):
	return render(response, "")