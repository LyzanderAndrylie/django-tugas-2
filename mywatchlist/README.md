# Aplikasi Mywatchlist Django
:link: [Aplikasi Mywatchlist](https://django-tugas-2-lyz.herokuapp.com/mywatchlist/)

***
## JSON, XML, dan HTML

***
## Pentingnya Data Delivery

***
## Implementasi
1. Pembuatan Aplikasi `mywatchlist`<br>
Kita dapat membuat suatu aplikasi baru berupa `mywatchlist` di Django dengan menggunakan perintah berupa
    ```
    py manage.py startapp mywatchlist
    ```
    atau

    ```
    django-admin startapp mywatchlist
    ```

    Kemudian, kita harus mendaftarkan aplikasi `wishlist` ke dalam proyek Django kita. Hal ini dilakukan dengan menambahkan `'mywatchlist'` ke dalam variabel `INSTALLED_APPS` pada `settings.py` pada folder `project_django`

    ```python
    INSTALLED_APPS = [
    ...,
    'mywatchlist',
    ]
    ``` 

2. Penambahan path `mywatchlist`<br>
Penambahan path bertujuan agar pengguna bisa mengakses https://django-tugas-2-lyz.herokuapp.com/mywatchlist/. Implementasi dilakukan dengan menambahkan `path('mywatchlist/', include('mywatchlist.urls')),` pada variable `urlpatterns` pada `urls.py` pada folder `project_django`.

    ```python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        ...,
        path('mywatchlist/', include('mywatchlist.urls')),
    ]
    ```

3. Pembuatan model `MyWatchList`<br>
Pembuatan model dilakukan dengan mendefinisikan suatu `class` bernama `MyWatchList` pada `models.py` pada folder `mywatchlist`. `Class` tersebut merupakan *subclass* dari `django.db.models.Model`. Kemudian, pada class tersebut, kita mendefinisikan attribut yang merepresentasikan *database field*. Implementasi kode berupa

    ```python
    from django.db import models

    # Create your models here.
    class MyWatchList(models.Model):
        watched = models.BooleanField()
        title = models.CharField(max_length=50)
        rating = models.IntegerField()
        release_date = models.DateField()
        review = models.TextField()
    ```

    > Perhatikan bahwa masing-masing *attribute*, yaitu `watched, title, rating, release_date, dan review` memiliki *field type* yang berbeda-beda (sesuai dengan ketentuan dari masing-masing *attribute* tersebut)

    Ketentuan mengenai masing-masing *attribute* berupa
    - `watched` untuk mendeskripsikan film tersebut sudah ditonton atau belum
    - `title` untuk mendeskripsikan judul film
    - `rating` untuk mendeskripsikan *rating* film dalam rentang 1 sampai dengan 5
    - `release_date` untuk mendeskripsikan kapan film dirilis
    - `review` untuk mendeskripsikan *review* untuk film tersebut

4. Penambahan 10 data untuk objek `MyWatchList`<br>
Penambahan dilakukan dengan membuat `initial_catalog_data.json` pada folder `fixtures` dan isi dengan kode berikut.
    ```json
    [
        {
            "model": "mywatchlist.mywatchlist",
            "pk": 1,
            "fields": {
                "watched": true,
                "title": "Interstellar",
                "rating": 5,
                "release_date": "2014-11-06",
                "review": "Film..."
            }
        },
        
        // dst.
    ]
    ```

    Kemudian, jangan lupa untuk *load* data tersebut ke *database* Django lokal dengan perintah `python manage.py loaddata initial_catalog_data.json`

5. Implementasi Fitur untuk Menyajikan Data dengan Format HTML, XML, dan JSON
Implementasi dilakukan dengan membuat fungsi pada `views.py` pada folder `mywatchlist` dengan kode sebagai berikut.
    ```python
    from django.shortcuts import render
    from mywatchlist.models import MyWatchList

    from django.http import HttpResponse
    from django.core import serializers

    # Fungsi untuk menyajikan data dalam bentuk HTML
    def show_mywatchlist(request):
        data_mywatchlist = MyWatchList.objects.all()
        context = {
            'mywatchlist': data_mywatchlist,
            'nama': 'Lyzander Marciano Andrylie',
            'id': '2106750755'
        }

        return render(request, "mywatchlist.html", context)

    # Fungsi untuk menyajikan data dalam bentuk XML
    def show_xml(request):
        data = MyWatchList.objects.all()

        return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

    # Fungsi untuk menyajikan data dalam bentuk JSON
    def show_json(request):
        data = MyWatchList.objects.all()

        return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    ```

6. Pembuatan *Routing*<br> 
Tujuan pembuatan *routing* adalah agar data di atas dapat diakses melalui URL yang sesuai. Hal ini dilakukan dengan menambahkan `path()` ke dalam variabel `urlpatterns` pada `urls.py` pada folder `mywatchlist`. Penambahan sebagai berikut.
    -  `path('html/', show_mywatchlist, name='show_mywatchlist')`<br>
    Untuk mengakses mywatchlist dalam format HTML pada http://localhost:8000/mywatchlist/html atau https://django-tugas-2-lyz.herokuapp.com/mywatchlist/html
    - `path('xml/', show_xml, name='show_xml')`<br>
    Untuk mengakses mywatchlist dalam format XML pada http://localhost:8000/mywatchlist/xml atau https://django-tugas-2-lyz.herokuapp.com/mywatchlist/xml
    - `path('json/', show_json, name='show_json')`<br>
    Untuk mengakses mywatchlist dalam format JSON pada http://localhost:8000/mywatchlist/json atau https://django-tugas-2-lyz.herokuapp.com/mywatchlist/json

    ```python
    from django.urls import path
    from mywatchlist.views import *

    app_name = 'mywatchlist'

    urlpatterns = [
        path('', show_menu, name='show_menu'),
        path('html/', show_mywatchlist, name='show_mywatchlist'),
        path('xml/', show_xml, name='show_xml'),
        path('json/', show_json, name='show_json'),
    ]
    ```

7. *Deployment* ke HeroKu untuk aplikasi `mywatchlist`<br>
*Deployment* bertujuan agar aplikasi `mywatchlist` dapat diakses melalui internet. Kita akan memanfaatkan *runner* dari GitHub Actions dan Heroku sebagai *host* dari aplikasi yang akan kita *deploy*.

    Perhatikan bahwa proses *deployment* telah dilakukan pada tugas sebelumnya, yaitu tugas 2. Oleh karena itu, untuk aplikasi `mywatchlist` kita tinggal menyesuaikan `Procfile` pada proyek Django kita agar data kita dapat ditampilkan dalam bentuk HTML, XML, dan JSON melalui internet.

    ```
    release: sh -c 'python manage.py migrate && python manage.py loaddata initial_catalog_data.json && python manage.py loaddata initial_mywatchlist_data.json'
    web: gunicorn project_django.wsgi --log-file -
    ```
