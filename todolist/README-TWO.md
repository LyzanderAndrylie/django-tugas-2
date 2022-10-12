# Aplikasi Todolist Django
:link: [Aplikasi Todolist](https://django-tugas-2-lyz.herokuapp.com/todolist)

## Perbedaan antara asynchronous programming dengan synchronous programming
| Asynchronous Programming | Synchronous Programming |
| ----------- | ----------- |
| Operasi atau program bisa berjalan secara paralel | Operasi  dijalankan secara sekuensial (satu pada satu waktu tertentu) |
| Operasi bersifat independen/tidak terikat satu sama lain | Operasi bersifat dependen/terikat satu sama lain |
| Multithreaded model | Single-thread model |
| Menggunakan non-blocking architecture | Menggunakan blocking architecture |
| Non-blocking -> dapat mengirim banyak request ke server dalam satu waktu | Blocking -> hanya dapat mengirim satu request ke server dalam satu waktu |
| Diaplikasikan pada networking dan komunikasi | Diaplikasikan pada reactive system |
| Meningkatkan throughput karena beberapa operasi dapat berjalan dalam waktu yang sama | Synchronous lebih lambat dibandingkan dengan asynchronous |

Sumber: 
- https://www.mendix.com/blog/asynchronous-vs-synchronous-programming/
- https://medium.com/codex/synchronous-vs-asynchronous-programming-4897070d640

***

## Penerapan Paradigma Event-Driven Programming pada JavaScript dan AJAX
Event-driven Programming adalah paradigma pemrograman yang fokus pada suatu event dengan alur dari sebuah program tersebut akan bergantung pada event yang terjadi. Event tersebut bisa berupa aksi dari user, seperti button yang diklik dan key tertentu pada keyboard ditekan.

Event-driven Programming bergantung pada *event loop* yang selalu menunggu event-event yang akan datang. Pada suatu event loop, event yang terjadi akan menentukan apa yang harus dieksekusi dan dengan urutan bagaimana.

Sumber: https://www.tutorialspoint.com/concurrency_in_python/concurrency_in_python_eventdriven_programming.htm

### Contoh Penerapan pada Aplikasi Todolist
```html
$("#form-add-task").submit(function(e) {
      e.preventDefault() // mencegah perilaku default browser untuk submisi form

      $.ajax({
        type: "POST",
        url: "{% url 'todolist:add_todolist_item' %}",
        data: $(this).serialize(), // Mendapatkan form data
        success: function(response) {
          
          // Append
          var htmlString = "";
          var task = response[0].fields
          
          if (task.is_finished) {
            htmlString = `
            <div class="card text-bg-success m-3 done" style="width: 18rem;">
              <div class="card-body">
                <h5 class="card-title">${task.title}</h5>
                <h6 class="card-subtitle mb-2">${task.date}</h6>
                <h6 class="card-subtitle mb-2">Selesai</h6>
                <p class="card-text">${task.description}</p>
                </div>
                </div>
                `
              } else {
                htmlString = `
                <div class="card text-bg-danger m-3 undone" style="width: 18rem;">
                  <div class="card-body">
                    <h5 class="card-title">${task.title}</h5>
                    <h6 class="card-subtitle mb-2">${task.date}</h6>
                    <h6 class="card-subtitle mb-2">Belum Selesai</h6>
                    <p class="card-text">${task.description}</p>
                    </div>
                    </div>
                    `
                  }
                  
          $("div#todolist-card").append(htmlString)
        }
      })      
    })
```
> Event akan terjadi ketika button submit pada form ditekan oleh pengguna. Ketika button submit tersebut ditekan, maka fungsi yang ada di dalam method submit() akan dijalankan (di-*trigger*), yaitu melakukan AJAX POST. Selanjutnya, ketika POST berhasil, daftar task pada halaman utama `todolist` akan diperbarui.

***

## Penerapan Asynchronous Programming pada AJAX.
Asynchronous Programming pada AJAX memungkinkan untuk berkomunikasi dengan server, bertukar data, dan memperbarui halaman web tanpa harus memuat ulang halaman web. Dengan hal ini, kita bisa bekerja dengan data dari dan/atau ke server tanpa harus menunggu respon dari server terlebih dahulu untuk melakukan *task* lainnya.

Salah satu penerapan Asynchronous Programming pada AJAX adalah AJAX GET dan AJAX POST.
```html
<!-- AJAX GET -->
$.ajax({
      url: "{% url 'todolist:show_json' %}",
      type: "GET",
      success: function(result) {
        ...
    })
```

```html
<!-- AJAX POST -->
$.ajax({
        type: "POST",
        url: "{% url 'todolist:add_todolist_item' %}",
        data: $(this).serialize(),
        success: function(response) {
            ...
        }
      }) 
```

***

## Implementasi
- AJAX GET
1. Pembuatan view yang mengembalikan seluruh data task dalam bentuk JSON<br>
Pembuatan view dilakukan sebagai berikut.
    ```python
    def show_json(request):
    user = request.user

    if user.is_authenticated:
        data = Task.objects.filter(user=user)
    else:
        data = Task.objects.all()

    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
    ```
    > Data task dalam bentuk JSON yang dikembalikan pada implementasi di atas tergantung pada pengguna. Jika pengguna telah login, data task dalam bentuk JSON yang dikembalikan hanya milik pengguna. Namun, jika belum ada pengguna yang login, data task dalam bentuk JSON yang dikembalikan adalah seluruh data task yang ada.

2. Pembuatan path `/todolist/json` yang mengarah ke view di atas<br>
Pembuatan dilakukan dengan menambahkan `path()` pada `urls.py` untuk aplikasi `todolist`.
    ```python
    urlpatterns = [
        ...
        path('json/', show_json, name='show_json'),
        ...
    ]
    ```
3. Pengambilan task menggunakan AJAX GET<br>
Pengambilan task dilakukan dengan kode berikut.
    ```html
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js"></script>
    <script>
    $(document).ready(function() {
        $.ajax({
            url: "{% url 'todolist:show_json' %}",
            type: "GET",
            success: function(result) {
                ...
            }
        })
    })
    </script>
    ```
    > `<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js"></script>` bertujuan untuk menggunakan JQuery dengan memanfaatkan google CDN (Content Delivery Network)

    - `ready()` method bertujuan untuk membuat fungsi tersedia ketika dokumen telah dimuat. 
    - `$.ajax()` bertujuan untuk melakukan AJAX request secara asinkronus. 
    - Parameter `result` berupa `Array` yang berisi data-data task 

    Selanjutnya, untuk menampilkan task yang telah diambil (GET) menggunakan AJAX GET, kita mendefinisikan *anonymous function* pada `success` yang berisi kode untuk menampilkan task-task tersebut.

    ```html
    <script>
    ...
    var htmlString = ''

    for (let index = 0; index < result.length; index++) {
          var task = result[index].fields;

          if (task.is_finished) {
            htmlString += `
            <div class="card text-bg-success m-3 done" style="width: 18rem;">
              <div class="card-body">
                <h5 class="card-title">${task.title}</h5>
                <h6 class="card-subtitle mb-2">${task.date}</h6>
                <h6 class="card-subtitle mb-2">Selesai</h6>
                <p class="card-text">${task.description}</p>
              </div>
            </div>
            `
          } else {
            htmlString += `
            <div class="card text-bg-danger m-3 undone" style="width: 18rem;">
              <div class="card-body">
                <h5 class="card-title">${task.title}</h5>
                <h6 class="card-subtitle mb-2">${task.date}</h6>
                <h6 class="card-subtitle mb-2">Belum Selesai</h6>
                <p class="card-text">${task.description}</p>
              </div>
            </div>
            `
          }
        }
        $("div#todolist-card").append(htmlString)  
        ...
        </script>
    ```

- AJAX POST
1. Pembuatan modal dengan form<br>
Pembuatan modal dengan form bertujuan untuk menambahkan task dengan memanfaatkan modal. Implementasi dilakukan dengan memanfaatkan modal Bootstrap.
    ```html
    <div class="d-grid gap-2 col-6 mx-auto my-3">

        <!-- Button trigger modal -->
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
        Add Task
        </button>

        <!-- Modal -->
        <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="staticBackdropLabel">Add Task</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form method="POST" id="form-add-task">  
                {% csrf_token %}  
                <table>  
                    {{ form.as_table }}  
                </table>  
                </div>
                <div class="modal-footer">
                <button type="submit" class="btn btn-success" data-bs-dismiss="modal">Add</button>
                </form>
            </div>
            </div>
        </div>
        </div>

        <button class="btn btn-success"><a href="{% url 'todolist:create_task' %}" class="link-light">Tambah Task Baru pada Halaman Baru</a></button>
        <button class="btn btn-danger"><a href="{% url 'todolist:logout' %}" class="link-light">Logout</a></button>
    </div>
    ```
2. Pembuatan view baru pada `views.py`<br>
Pembuatan view baru bertujuan untuk menambahkan task baru ke dalam *database*. Implementasi dilakukan sebagai berikut.
    ```python
    def add_todolist_item(request):
        if request.method == 'POST':
            form = TaskForm(request.POST)

            if form.is_valid():
                # Pembuatan objek dari model Task
                user = request.user
                date = datetime.datetime.now()

                data = form.cleaned_data
                title = data['judul_task']
                description = data['deskripsi_task']

                # Simpan objek dari model Task ke database
                task = Task(user=user, date=date, title=title, description=description)
                task.save()

                # Mendapatkan objek dari database
                task_set = Task.objects.filter(pk=task.pk)

                # Mengubah objek menjadi format JSON
                task_json = serializers.serialize('json', task_set)

            # Mengembalikan task yang telah dibuat 
            return HttpResponse(task_json, content_type="text/json")

        return HttpResponseNotFound()
    ```
    > Perhatikan HTTP Reponse berupa `Array` yang berisi objek task dalam format JSON yang baru ditambahkan

3. Pembuatan path `/todolist/add` yang mengarah ke view di atas<br>
Pembuatan dilakukan dengan menambahkan `path()` pada `urls.py` untuk aplikasi `todolist`.
    ```python
    urlpatterns = [
        ...
         path('add/', add_todolist_item, name='add_todolist_item'),
        ...
    ]
    ```

4. Penghubungan form di dalam modal dengan path `/todolist/add`<br>
Implementasi dilakukan dengan memanfaatkan AJAX POST dan mengatur url berupa `"{% url 'todolist:add_todolist_item' %}"`.
    ```html
    $("#form-add-task").submit(function(e) {
        e.preventDefault() // mencegah perilaku default browser untuk submisi form

        $.ajax({
            type: "POST",
            url: "{% url 'todolist:add_todolist_item' %}",
            data: $(this).serialize(), // Mendapatkan form data
            success: function(response) {
                ...
            }
        })      
    })
    ```

5. Menutup modal setelah penambahan task berhasil dilakukan<br>
Implementasi dilakukan dengan menambahkan atribut `data-bs-dismiss="modal"` di tombol Add pada modal.

    ```html
    <button type="submit" class="btn btn-success" data-bs-dismiss="modal">Add</button>
    ```

6. *Refresh* Halaman utama secara asinkronus<br>
*Refresh* halaman utama secara asinkronus dilakukan untuk menampilkan list task terbaru tanpa *reload* seluruh page. Pembaruan dilakukan dengam menambahkan task yang baru dibuat. Implementasi dilakukan sebagai berikut.
    ```html
    $.ajax({
            type: "POST",
            url: "{% url 'todolist:add_todolist_item' %}",
            data: $(this).serialize(), // Mendapatkan form data
            success: function(response) {
            
            // Append
            var htmlString = "";
            var task = response[0].fields
            
            if (task.is_finished) {
                htmlString = `
                <div class="card text-bg-success m-3 done" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">${task.title}</h5>
                    <h6 class="card-subtitle mb-2">${task.date}</h6>
                    <h6 class="card-subtitle mb-2">Selesai</h6>
                    <p class="card-text">${task.description}</p>
                    </div>
                    </div>
                    `
                } else {
                    htmlString = `
                    <div class="card text-bg-danger m-3 undone" style="width: 18rem;">
                    <div class="card-body">
                        <h5 class="card-title">${task.title}</h5>
                        <h6 class="card-subtitle mb-2">${task.date}</h6>
                        <h6 class="card-subtitle mb-2">Belum Selesai</h6>
                        <p class="card-text">${task.description}</p>
                        </div>
                        </div>
                        `
                    }
                    
            $("div#todolist-card").append(htmlString)
            }
        }) 
    ```
    > HTTP Reponse berupa `Array` yang berisi objek task dalam format JSON yang baru ditambahkan diassign pada parameter `response`. Dengan demikian, kita dapat memanfaatkan parameter `response` untuk memperbarui daftar task kita.
