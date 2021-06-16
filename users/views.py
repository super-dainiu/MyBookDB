from django.shortcuts import render, redirect
from login.models import User as user
from .models import *
from django.db import transaction

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
# Create your views here.


def index(request):
    info = {"fields": User._meta.fields, "users": {}}
    if not(user.objects.filter(ip=request.META['REMOTE_ADDR'])):
        return redirect("../")
    name_filter = ''
    address_filter = ''
    email_filter = ''
    id_filter = ''
    orderby = ''
    orderby2 = ''
    order = ''
    order2 = ''
    delete_id = None
    if request.method == "GET":
        name_filter = request.GET.get('name') if request.GET.get('name') else ''
        address_filter = request.GET.get('address') if request.GET.get('address') else ''
        email_filter = request.GET.get('email') if request.GET.get('email') else ''
        id_filter = request.GET.get('id') if request.GET.get('id') else ''
        orderby = request.GET.get('orderby')
        order = request.GET.get('order')
        orderby2 = request.GET.get('orderby2')
        order2 = request.GET.get('order2')
        delete_id = request.GET.get('delete')
        info.update({"name_filter": name_filter, "address_filter": address_filter, "orderby": orderby, "order": order,
                     "orderby2": orderby2, "order2": order2, "email_filter": email_filter, "id_filter": id_filter})
    if delete_id:
        User.objects.filter(id=delete_id).delete()
    orders = []
    if orderby:
        if order == "asc":
            orders.append(orderby)
        if order == "desc":
            orders.append('-'+orderby)
    if orderby2:
        if order2 == "asc":
            orders.append(orderby2)
        if order2 == "desc":
            orders.append('-'+orderby2)
    if id_filter:
        info.update({"users": User.objects.filter(name__icontains=name_filter, address__icontains=address_filter,
                                              email__icontains=email_filter, id=int(id_filter)).order_by(*orders)})
    else:
        info.update({"users": User.objects.filter(name__icontains=name_filter, address__icontains=address_filter,
                                                  email__icontains=email_filter).order_by(*orders)})
    return render(request, 'users.html', info)


def create(request):
    info = {}
    if not(user.objects.filter(ip=request.META['REMOTE_ADDR'])):
        return redirect("../")
    if request.method == "POST":
        name = request.POST.get("name")
        sex = request.POST.get("sex")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        vip = request.POST.get("vip")
        info.update({'name': name, 'sex': sex, 'phone': phone, 'email': email, 'address': address, 'vip': vip})
        if User.objects.filter(name=name):
            info.update({"nameerr": "Already exists %s"%name})
            info.pop('name')
            return render(request, 'edituser.html', info)
        if User.objects.filter(phone=phone):
            info.update({"phoneerr": "Phone number already used by %s" % User.objects.get(phone=phone).name})
            info.pop('phone')
            return render(request, 'edituser.html', info)
        if User.objects.filter(email=email):
            info.update({"emailerr": "Email already used by %s" % User.objects.get(email=email).name})
            info.pop('email')
            return render(request, 'edituser.html', info)
        new=User.objects.create(name=name, phone=phone, email=email, sex=sex, address=address, vip=bool(vip))
        return redirect('../?id=%d'%new.id)
    return render(request, 'edituser.html', info)


def edit(request, userid):
    if not(user.objects.filter(ip=request.META['REMOTE_ADDR'])):
        return redirect("../")
    with transaction.atomic():
        target = User.objects.select_for_update(skip_locked=True).get(id=userid)
        info = {'name': target.name, 'sex': target.sex, 'phone': target.phone, 'email': target.email,
                'address': target.address, 'vip': str(target.vip)}
        if request.method == "POST":
            name = request.POST.get("name")
            sex = request.POST.get("sex")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            address = request.POST.get("address")
            vip = request.POST.get("vip")
            info.update({'name': name, 'sex': sex, 'phone': phone, 'email': email, 'address': address, 'vip': vip})
            if User.objects.filter(name=name).exclude(id=userid):
                info.update({"nameerr": "Already exists %s" % name})
                info['name']=target.name
                return render(request, 'edituser.html', info)
            if User.objects.filter(phone=phone).exclude(id=userid):
                info.update({"phoneerr": "Phone number already used by %s" % User.objects.get(phone=phone).name})
                info['phone']=target.phone
                return render(request, 'edituser.html', info)
            if User.objects.filter(email=email).exclude(id=userid):
                info.update({"emailerr": "Email already used by %s" % User.objects.get(email=email).name})
                info['email']=target.email
                return render(request, 'edituser.html', info)
            target.name=name
            target.phone=phone
            target.email=email
            target.sex=sex
            target.address=address
            target.vip=bool(vip)
            target.save()
            return redirect('../?id=%d'%userid)
        return render(request, 'edituser.html', info)
