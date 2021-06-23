from django.shortcuts import render, redirect
from login.models import User
from users.models import User as us
from .models import *
from django.db import transaction
from orders.models import Details


# Create your views here.


def index(request):
    info = {"fields": Orders._meta.fields}
    if not (User.objects.filter(ip=request.META['REMOTE_ADDR'])):
        return redirect("../")
    id_filter = ''
    date_filter = ''
    user_filter = ''
    lastedit_filter = ''
    confirmed_filter = ''
    orderby = ''
    orderby2 = ''
    order = ''
    order2 = ''
    confirm_id = None
    if request.method == "GET":
        user_filter = request.GET.get('user') if request.GET.get('user') else ''
        id_filter = request.GET.get('id') if request.GET.get('id') else ''
        date_filter = request.GET.get('date') if request.GET.get('date') else ''
        book_filter = request.GET.get('book') if request.GET.get('book') else ''
        lastedit_filter = request.GET.get('lastedit') if request.GET.get('lastedit') else ''
        confirmed_filter = request.GET.get('confirmed') if request.GET.get('confirmed') else ''
        orderby = request.GET.get('orderby')
        order = request.GET.get('order')
        orderby2 = request.GET.get('orderby2')
        order2 = request.GET.get('order2')
        confirm_id = request.GET.get('confirm')
        info.update(
            {"user_filter": user_filter, "orderby": orderby, "order": order,
             "lastedit": lastedit_filter, "book_filter": book_filter, "confirm_filter": confirmed_filter,
             "orderby2": orderby2, "order2": order2, "id_filter": id_filter, "date_filter": date_filter})

    if confirm_id:
        my_order = Orders.objects.get(id=confirm_id)
        if my_order.confirm == "0":
            enough = 1
            user_now = User.objects.filter(ip=request.META['REMOTE_ADDR']).first()
            for book, detail in zip(my_order.book.all(), my_order.details_set.all()):
                count = detail.count
                if book.storage < count:
                    info.update({"message": "Not enough storage for %s" % book})
                    enough = 0
            if enough:
                for book, detail in zip(my_order.book.all(), my_order.details_set.all()):
                    count = detail.count
                    book.storage -= count
                    book.save()
                my_order.confirm = '1'
                my_order.lastedit = user_now
                my_order.save()

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
    if id_filter and date_filter:
        info.update(
            {"orders": Orders.objects.filter(date=date_filter, id=int(id_filter)).order_by(*orders)})
    elif id_filter:
        info.update(
            {"orders": Orders.objects.filter(id=int(id_filter)).order_by(*orders)})
    elif date_filter:
        info.update(
            {"orders": Orders.objects.filter(date=date_filter).order_by(*orders)})
    else:
        if lastedit_filter:
            info.update(
                {"orders": Orders.objects.filter(user__name__icontains=user_filter,
                                                 lastedit__username__icontains=lastedit_filter,
                                                 confirm__icontains=confirmed_filter).order_by(*orders)})
        else:
            info.update(
                {"orders": Orders.objects.filter(user__name__icontains=user_filter,
                                                 confirm__icontains=confirmed_filter).order_by(*orders)})
    return render(request, 'orders.html', info)

