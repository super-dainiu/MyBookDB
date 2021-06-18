from django.shortcuts import render, redirect
from login.models import User
from .models import *
from django.db import transaction

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
# Create your views here.


def index(request):
    info = {"fields": Writers._meta.fields, "writers": {}}
    if not(User.objects.filter(ip=request.META['REMOTE_ADDR'])):
        return redirect("../")
    name_filter = ''
    author_type_filter = ''
    id_filter = ''
    orderby = ''
    orderby2 = ''
    order = ''
    order2 = ''
    delete_id = None
    if request.method == "GET":
        name_filter = request.GET.get('name') if request.GET.get('name') else ''
        author_type_filter = request.GET.get('author_type') if request.GET.get('author_type') else ''
        id_filter = request.GET.get('id') if request.GET.get('id') else ''
        orderby = request.GET.get('orderby')
        order = request.GET.get('order')
        orderby2 = request.GET.get('orderby2')
        order2 = request.GET.get('order2')
        delete_id = request.GET.get('delete')
        info.update({"name_filter": name_filter,  "orderby": orderby, "order": order,
                     "orderby2": orderby2, "order2": order2, "author_type_filter": author_type_filter, "id_filter": id_filter})
    if delete_id:
        Writers.objects.filter(id=delete_id).delete()
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
    if id_filter and author_type_filter:
        info.update({"writers": Writers.objects.filter(name__icontains=name_filter,
                                                       author_type=author_type_filter,
                                                       id=int(id_filter)).order_by(*orders)})
    elif id_filter:
        info.update({"writers": Writers.objects.filter(name__icontains=name_filter,
                                                       id=int(id_filter)).order_by(*orders)})
    elif author_type_filter:
        info.update({"writers": Writers.objects.filter(name__icontains=name_filter,
                                                       author_type=author_type_filter).order_by(*orders)})
    else:
        info.update({"writers": Writers.objects.filter(name__icontains=name_filter).order_by(*orders)})
    return render(request, 'writers.html', info)


def create(request):
    info = {}
    if not(User.objects.filter(ip=request.META['REMOTE_ADDR'])):
        return redirect("../")
    if request.method == "POST":
        name = request.POST.get("name")
        author_type = request.POST.get("author_type")
        info.update({'name': name, 'author_type': author_type})
        if Writers.objects.filter(name=name, author_type=author_type):
            info.update({"nameerr": "Already exists %s as %s" % (name, author_type)})
            info.pop('name')
            return render(request, 'editwriter.html', info)
        new = Writers.objects.create(name=name, author_type=author_type)
        return redirect('../?id=%d' % new.id)
    return render(request, 'editwriter.html', info)


def edit(request, writerid):
    if not(User.objects.filter(ip=request.META['REMOTE_ADDR'])):
        return redirect("../")
    with transaction.atomic():
        target = Writers.objects.select_for_update(skip_locked=True).get(id=writerid)
        info = {'name': target.name, 'author_type': target.author_type}
        if request.method == "POST":
            name = request.POST.get("name")
            author_type = request.POST.get("author_type")
            info.update({'name': name, 'author_type': author_type})
            if Writers.objects.filter(name=name, author_type=author_type).exclude(id=writerid):
                info.update({"nameerr": "Already exists %s as %s" % (name,author_type)})
                info['name'] = target.name
                return render(request, 'editwriter.html', info)
            target.name = name
            target.author_type = author_type
            target.save()
            return redirect('../?id=%d' % writerid)
        return render(request, 'editwriter.html', info)
