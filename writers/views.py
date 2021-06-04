from django.shortcuts import render
from login.models import User

# Create your views here.


def index(request):
    if User.objects.filter(ip=request.META['REMOTE_ADDR']):
        return render(request, 'writers.html')
    else:
        return redirect("../")
