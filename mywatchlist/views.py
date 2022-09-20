from django.shortcuts import render
from mywatchlist.models import MyWatchList

from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def show_menu(request):
    context = {
        "html_path": "./html",
        "xml_path": "./xml",
        "json_path": "./json"
    }

    return render(request, 'menu.html', context)

def show_mywatchlist(request):
    data_mywatchlist = MyWatchList.objects.all()
    message = message_based_on_total_watch(data_mywatchlist)
    context = {
        'mywatchlist': data_mywatchlist,
        'nama': 'Lyzander Marciano Andrylie',
        'id': '2106750755',
        'pesan': message
    }

    return render(request, "mywatchlist.html", context)

def message_based_on_total_watch(data):
    watched = 0
    not_watched = 0

    for film in data:
        if film.watched:
            watched += 1
        else:
            not_watched += 1

    if watched >= not_watched:
        return "Selamat, kamu sudah banyak menonton!"
    else:
        return "Wah, kamu masih sedikit menonton!"


def show_xml(request):
    data = MyWatchList.objects.all()

    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = MyWatchList.objects.all()

    return HttpResponse(serializers.serialize("json", data), content_type="application/json")