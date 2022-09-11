from django.shortcuts import render
from katalog.models import CatalogItem

# TODO: Create your views here.
def show_katalog(request):
    data_katalog = CatalogItem.objects.all()
    context = {
        'list_item': data_katalog,
        'nama': 'Lyzander Marciano Andrylie',
        'id': '2106750755',
    }

    return render(request, "katalog.html", context)