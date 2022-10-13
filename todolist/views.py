from multiprocessing import context
from os import stat
from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from urllib3 import HTTPResponse
from todolist.models import Task

import datetime
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

from todolist.forms import TaskForm

from django.http import HttpResponse
from django.core import serializers

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required(login_url='/todolist/login/')
def show_todolist(request):
    user = request.user
    username = ""

    # Pengecekan user
    if user.is_authenticated:
        username = user.username

    data_task = Task.objects.filter(user=user)
    form = TaskForm()
    
    context = {
        'data_task': data_task,
        'nama_user': username,
        'nama': 'Lyzander Marciano Andrylie',
        'id': '2106750755',
        'form': form,
    }
    return render(request, 'todolist.html', context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('todolist:show_todolist')
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('todolist:login')

def create_task(request):
    form = TaskForm()

    print(request.POST)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        print(request.POST)

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

            return redirect('todolist:show_todolist')

    # Pengecekan user
    user = request.user
    username = ""

    if user.is_authenticated:
        username = user.username

    context = {
        'nama_user': username,
        'nama': 'Lyzander Marciano Andrylie',
        'id': '2106750755',
        'form': form
    }
    
    return render(request, "create_task.html", context)

def update_task(request, id):
    task = Task.objects.get(pk=id)
    ubah_status = not task.is_finished
    Task.objects.filter(pk=id).update(is_finished=ubah_status)

    return redirect('todolist:show_todolist')

def delete_task(request, id):
    task = Task.objects.get(pk=id)
    task.delete()

    return redirect('todolist:show_todolist')

def show_about(request):
    return render(request, "about.html")

def show_json(request):
    user = request.user

    if user.is_authenticated:
        data = Task.objects.filter(user=user)
    else:
        data = Task.objects.all()

    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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

@csrf_exempt
def delete_todolist_item(request, id):
    if request.method == 'DELETE':
        print(id)
        task = Task.objects.get(pk=id)
        task.delete()

        return HttpResponse('Deleted')
    
    return HttpResponseNotFound()