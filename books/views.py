from django.db import transaction
from django.shortcuts import render, redirect

from django.utils.timezone import now
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
    writer_filter = ''
    publisher_filter = ''
    classification_filter = ''
    sub_classification_filter = ''
    delete_id = None
    if request.method == "GET":
        title_filter = request.GET.get('title') if request.GET.get('title') else ''
        writer_filter = request.GET.get('writer') if request.GET.get('writer') else ''
        publisher_filter = request.GET.get('publisher') if request.GET.get('publisher') else ''
        id_filter = request.GET.get('id') if request.GET.get('id') else ''
        classification_filter = request.GET.get('classification') if request.GET.get('classification') else ''
        sub_classification_filter = request.GET.get('sub_classification') if request.GET.get('sub_classification') else ''
        orderby = request.GET.get('orderby')
        order = request.GET.get('order')
        orderby2 = request.GET.get('orderby2')
        order2 = request.GET.get('order2')
        delete_id = request.GET.get('delete')
        info.update(
            {"title_filter": title_filter, "writer_filter": writer_filter, "orderby": orderby, "order": order,
             "classification_filter": classification_filter, 'sub_classification_filter': sub_classification_filter,
             "orderby2": orderby2, "order2": order2, "publisher_filter": publisher_filter, "id_filter": id_filter})
    if delete_id:
        Books.objects.filter(id=delete_id).delete()
    orders = []
    if orderby and orderby:
        if order == "asc":
            orders.append(orderby)
        if order == "desc":
            orders.append('-' + orderby)
    if orderby2 and orderby2:
        if order2 == "asc":
            orders.append(orderby2)
        if order2 == "desc":
            orders.append('-' + orderby2)
    if not orders:
        orders = ['id']
    if id_filter:
        info.update({"books": Books.objects.filter(
            id=int(id_filter), title__icontains=title_filter, publishers__name__icontains=publisher_filter,
            writers__name__icontains=writer_filter, classification__class_name__icontains=classification_filter,
            sub_classification__class_name__icontains=sub_classification_filter)
            .distinct().order_by(*orders)})
    else:
        info.update({"books": Books.objects.filter(title__icontains=title_filter,
                                                   publishers__name__icontains=publisher_filter,
                                                   writers__name__icontains=writer_filter,
                                                   classification__class_name__icontains=classification_filter,
                                                   sub_classification__class_name__icontains=sub_classification_filter).distinct()
                    .order_by(*orders)})
    return render(request, 'books.html', info)


def create(request):
    info = {'publish_date': now().date().isoformat()}
    if request.method == "POST":
        title = request.POST.get("title")
        writers = request.POST.get("writers")
        authors = []
        translators = []
        for item in writers.split(";"):
            if "[作]" in item:
                authors.append(item[3:])
            if "[译]" in item:
                translators.append(item[3:])
        price = request.POST.get("price")
        price_vip = request.POST.get("price_vip")
        publishers = request.POST.get("publishers")
        classification = request.POST.get("classification")
        publish_date = request.POST.get("publish_date")
        edition = request.POST.get("edition")
        storage = request.POST.get("storage")
        info.update(
            {'title': title, 'writers': writers, 'price': price, 'price_vip': price_vip, 'publishers': publishers,
             'classification': classification, 'publish_date': publish_date,
             'edition': edition, 'storage': storage})
        cate1, cate2 = classification.split("/")
        if not Publishers.objects.filter(name=publishers):
            info.update({"puberr": "No publisher named %s" % publishers})
            info['publishers'] = ''
            return render(request, 'editbooks.html', info)

        for author in authors:
            if not Writers.objects.filter(name=author, author_type="Author"):
                info.update({"writererr": "No author named %s" % author})
                return render(request, 'editbooks.html', info)
        for translator in translators:
            if not Writers.objects.filter(name=translator, author_type="Translator"):
                info.update({"writererr": "No translator named %s" % translator})
                return render(request, 'editbooks.html', info)

        if Books.objects.filter(title=title, publishers=Publishers.objects.get(name=publishers), edition=edition):
            info.update({"bookerr": "Already exists %s  from  %s" % (title, publishers)})
            return render(request, 'editbooks.html', info)

        new_cate = Classification.objects.get_or_create(class_name=cate1)[0]
        new_sub_cate = ClassificationSub.objects.get_or_create(class_name=cate2, ancestor_class_name=new_cate)[0]
        new = Books.objects.create(title=title, price=price, price_vip=price_vip,
                                   publishers=Publishers.objects.get(name=publishers),
                                   classification=new_cate, sub_classification=new_sub_cate,
                                   publish_date=publish_date,
                                   edition=edition, storage=storage)
        for author in authors:
            new.writers.add(Writers.objects.get(name=author, author_type='Author'))
        for translator in translators:
            new.writers.add(Writers.objects.get(name=translator, author_type='Translator'))
        return redirect('../?id=%d' % new.id)
    return render(request, 'editbooks.html', info)


def edit(request, bookid):
    info = {}
    with transaction.atomic():
        target = Books.objects.select_for_update(skip_locked=True).get(id=bookid)
        t_writers = ''
        for writer in target.writers.all():
            t_writers = t_writers + str(writer) + ';'
        info = {'title': target.title, 'price': target.price, 'price_vip': target.price_vip,
                'publishers': target.publishers,
                'classification': target.sub_classification, 'publish_date': str(target.publish_date),
                'edition': target.edition, 'storage': target.storage, 'writers': t_writers}
        if request.method == "POST":
            title = request.POST.get("title")
            writers = request.POST.get("writers")
            authors = []
            translators = []
            for item in writers.split(";"):
                if "[作]" in item:
                    authors.append(item[3:])
                if "[译]" in item:
                    translators.append(item[3:])
            price = request.POST.get("price")
            price_vip = request.POST.get("price_vip")
            publishers = request.POST.get("publishers")
            classification = request.POST.get("classification")
            publish_date = request.POST.get("publish_date")
            edition = request.POST.get("edition")
            storage = request.POST.get("storage")
            info.update(
                {'title': title, 'writers': writers, 'price': price, 'price_vip': price_vip, 'publishers': publishers,
                 'classification': classification, 'publish_date': publish_date,
                 'edition': edition, 'storage': storage})
            cate1, cate2 = classification.split("/")
            if not Publishers.objects.filter(name=publishers):
                info.update({"puberr": "No publisher named %s" % publishers})
                info['publishers'] = ''
                return render(request, 'editbooks.html', info)

            for author in authors:
                if not Writers.objects.filter(name=author, author_type="Author"):
                    info.update({"writererr": "No author named %s" % author})
                    info['writers'] = t_writers
                    return render(request, 'editbooks.html', info)
            for translator in translators:
                if not Writers.objects.filter(name=translator, author_type="Translator"):
                    info.update({"writererr": "No translator named %s" % translator})
                    info['writers'] = t_writers
                    return render(request, 'editbooks.html', info)

            if Books.objects.filter(title=title, publishers=Publishers.objects.get(name=publishers),
                                    edition=edition).exclude(id=bookid):
                info.update({"bookerr": "Already exists %s  from  %s" % (title, publishers)})
                return render(request, 'editbooks.html', info)

            new_cate = Classification.objects.get_or_create(class_name=cate1)[0]
            new_sub_cate = ClassificationSub.objects.get_or_create(class_name=cate2, ancestor_class_name=new_cate)[0]

            target.title = title
            target.price = price
            target.price_vip = price_vip
            target.publishers = Publishers.objects.get(name=publishers)
            target.classification = new_cate
            target.sub_classification = new_sub_cate
            target.publish_date = publish_date
            target.edition = edition
            target.storage = storage
            target.writers.clear()
            for author in authors:
                target.writers.add(Writers.objects.get(name=author, author_type='Author'))
            for translator in translators:
                target.writers.add(Writers.objects.get(name=translator, author_type='Translator'))
            target.save()
            return redirect('../?id=%d' % bookid)
        return render(request, 'editbooks.html', info)
