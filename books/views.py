from django.shortcuts import render, redirect
from login.models import User as user
from .models import *
from django.db import transaction

# Create your views here.


def index(request):

    return render(request, 'books.html')


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
        info = {'name': target.name, 'sex': target.sex, 'phone': target.phone, 'email': target.email,
                'address': target.address, 'vip': str(target.vip)}
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