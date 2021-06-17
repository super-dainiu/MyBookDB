from django.db import transaction
from django.shortcuts import render, redirect

from login.models import User
from publishers.models import Publishers
from writers.models import Writers
from .models import *


# Create your views here.


def index(request):
    info = {"fields": Books._meta.fields, "books": {}}
    if not (User.objects.filter(ip=request.META['REMOTE_ADDR'])):
        return redirect("../")
    title_filter = ''
    id_filter = ''
    orderby = ''
    orderby2 = ''
    order = ''
    order2 = ''
    delete_id = None
    if request.method == "GET":
        title_filter = request.GET.get('title') if request.GET.get('title') else ''
        writer_filter = request.GET.get('writer') if request.GET.get('writer') else ''
        publisher_filter = request.GET.get('publisher') if request.GET.get('publisher') else ''
        id_filter = request.GET.get('id') if request.GET.get('id') else ''
        classification_filter = request.GET.get('classification') if request.GET.get('classification') else ''
        orderby = request.GET.get('orderby')
        order = request.GET.get('order')
        orderby2 = request.GET.get('orderby2')
        order2 = request.GET.get('order2')
        delete_id = request.GET.get('delete')
        info.update(
            {"title_filter": title_filter, "writer_filter": writer_filter, "orderby": orderby, "order": order,
             "classification_filter": classification_filter,
             "orderby2": orderby2, "order2": order2, "publisher_filter": publisher_filter, "id_filter": id_filter})
    if delete_id:
        Books.objects.filter(id=delete_id).delete()
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
        info.update({"books": Books.objects.filter(
            id=int(id_filter, title__icontains=title_filter, publishers__name_icontains=publisher_filter,
                   writers__name__icontains=writer_filter)).order_by(*orders)})
    else:
        info.update({"books": Books.objects.filter(title__icontains=title_filter,
                                                   publishers__name__icontains=publisher_filter,
                                                   writers__name__icontains=writer_filter).order_by(*orders)})
    print(info)
    return render(request, 'books.html', info)


def create(request):
    info = {}
    if request.method == "POST":
        title = request.POST.get("title")
        writers = request.POST.get("writers")
        price = request.POST.get("price")
        price_vip = request.POST.get("price_vip")
        publishers = request.POST.get("publishers")
        classification = request.POST.get("classification")
        sub_classification = request.POST.get("sub_classification")
        publish_date = request.POST.get("publish_date")
        edition = request.POST.get("edition")
        storage = request.POST.get("storage")
        info.update(
            {'title': title, 'writers': writers, 'price': price, 'price_vip': price_vip, 'publishers': publishers,
             'classification': classification, 'sub_classification': sub_classification, 'publish_date': publish_date,
             'edition': edition, 'storage': storage})
        if Books.objects.filter(title=title) & Books.objects.filter(publishers=publishers) & Books.objects.filter(
                edition=edition):
            info.update({"bookerr": "Already exists %s" % title})
            return render(request, 'editbooks.html', info)
        new = Books.objects.create(title=title, writers=writers, price=price, price_vip=price_vip,
                                   publishers=publishers,
                                   classification=classification, sub_classification=sub_classification,
                                   publish_date=publish_date,
                                   edition=edition, storage=storage)
        return redirect('../?id=%d' % new.id)
    return render(request, 'editbooks.html', info)


def edit(request, bookid):
    with transaction.atomic():
        target = Books.objects.select_for_update(skip_locked=True).get(id=bookid)
        info = {'title': target.title, 'sex': target.sex, 'phone': target.phone, 'email': target.email,
                'writer': target.writer, 'vip': str(target.vip)}
        if request.method == "POST":
            title = request.POST.get("title")
            writers = request.POST.get("writers")
            price = request.POST.get("price")
            price_vip = request.POST.get("price_vip")
            publishers = request.POST.get("publishers")
            classification = request.POST.get("classification")
            sub_classification = request.POST.get("sub_classification")
            publish_date = request.POST.get("publish_date")
            edition = request.POST.get("edition")
            storage = request.POST.get("storage")
            info.update(
                {'title': title, 'writers': writers, 'price': price, 'price_vip': price_vip, 'publishers': publishers,
                 'classification': classification, 'sub_classification': sub_classification,
                 'publish_date': publish_date,
                 'edition': edition, 'storage': storage})

            if Books.objects.filter(title=title) & Books.objects.filter(publishers=publishers) & Books.objects.filter(
                    edition=edition):
                info.update({"bookerr": "Already exists %s" % title})
                return render(request, 'editbooks.html', info)

            target.title = title
            target.writers = writers
            target.price = price
            target.price_vip = price_vip
            target.publishers = publishers
            target.classification = classification
            target.sub_classification = sub_classification
            target.publish_date = publish_date
            target.edition = edition
            target.storage = storage
            target.save()
            return redirect('../?id=%d' % bookid)
        return render(request, 'editbooks.html', info)
