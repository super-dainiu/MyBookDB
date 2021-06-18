from django.shortcuts import render, redirect
from login.models import User
from .models import *
from django.db import transaction

# Create your views here.


def index(request):
    info = {"fields": Publishers._meta.fields, "publishers": {}}
    if not (User.objects.filter(ip=request.META['REMOTE_ADDR'])):
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
        info.update(
            {"name_filter": name_filter, "address_filter": address_filter, "orderby": orderby, "order": order,
             "orderby2": orderby2, "order2": order2, "email_filter": email_filter, "id_filter": id_filter})
    if delete_id:
        Publishers.objects.filter(id=delete_id).delete()
    orders = []
    if orderby:
        if order == "asc":
            orders.append(orderby)
        if order == "desc":
            orders.append('-' + orderby)
    if orderby2:
        if order2 == "asc":
            orders.append(orderby2)
        if order2 == "desc":
            orders.append('-' + orderby2)
    if id_filter:
        info.update(
            {"publishers": Publishers.objects.filter(name__icontains=name_filter, address__icontains=address_filter,
                                                     email__icontains=email_filter, id=int(id_filter)).order_by(*orders)})
    else:
        info.update(
            {"publishers": Publishers.objects.filter(name__icontains=name_filter, address__icontains=address_filter,
                                                     email__icontains=email_filter).order_by(*orders)})
    return render(request, 'publishers.html', info)


def create(request):
    info = {}
    if not (User.objects.filter(ip=request.META['REMOTE_ADDR'])):
        return redirect("../")
    if request.method == "POST":
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        contacts = request.POST.get("contacts")
        address = request.POST.get("address")
        info.update(
            {'name': name, 'phone_number': phone_number, 'email': email, 'contacts': contacts, 'address': address})
        if Publishers.objects.filter(name=name):
            info.update({"nameerr": "Already exists %s" % name})
            info.pop('name')
            return render(request, 'editpublishers.html', info)
        if Publishers.objects.filter(phone_number=phone_number):
            info.update({"phoneerr": "Phone number already used by %s" % Publishers.objects.get(phone_number=phone_number).name})
            info.pop('phone_number')
            return render(request, 'editpublishers.html', info)
        if Publishers.objects.filter(email=email):
            info.update({"emailerr": "Email already used by %s" % Publishers.objects.get(email=email).name})
            info.pop('email')
            return render(request, 'editpublishers.html', info)
        new = Publishers.objects.create(name=name, phone_number=phone_number, email=email, contacts=contacts, address=address)
        return redirect('../?id=%d' % new.id)
    return render(request, 'editpublishers.html', info)


def edit(request, publisherid):
    if not (User.objects.filter(ip=request.META['REMOTE_ADDR'])):
        return redirect("../")
    with transaction.atomic():
        target = Publishers.objects.select_for_update(skip_locked=True).get(id=publisherid)
        info = {'name': target.name, 'phone_number': target.phone_number, 'email': target.email,
                'contacts': target.contacts, 'address': target.address}
        if request.method == "POST":
            name = request.POST.get("name")
            phone_number = request.POST.get("phone_number")
            email = request.POST.get("email")
            contacts = request.POST.get("contacts")
            address = request.POST.get("address")

            info.update({'name': name,  'phone_number': phone_number, 'email': email, 'contacts': contacts, 'address': address})
            if Publishers.objects.filter(name=name).exclude(id=publisherid):
                info.update({"nameerr": "Already exists %s" % name})
                info['name']=target.name
                return render(request, 'editpublishers.html', info)
            if Publishers.objects.filter(phone_number=phone_number).exclude(id=publisherid):
                info.update({"phoneerr": "Phone number already used by %s" % Publishers.objects.get(phone_number=phone_number).name})
                info['phone_number']=target.phone_number
                return render(request, 'editpublishers.html', info)
            if Publishers.objects.filter(email=email).exclude(id=publisherid):
                info.update({"emailerr": "Email already used by %s" % Publishers.objects.get(email=email).name})
                info['email']=target.email
                return render(request, 'editpublishers.html', info)
            target.name=name
            target.phone_number=phone_number
            target.email=email
            target.address=address
            target.contacts=contacts
            target.save()
            return redirect('../?id=%d'%publisherid)
        return render(request, 'editpublishers.html', info)