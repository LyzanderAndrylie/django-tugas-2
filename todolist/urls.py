from django.urls import path
from todolist.views import delete_task, register, show_about

from todolist.views import *

app_name = 'todolist'

urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('update/<int:id>', update_task, name='update_task'),
    path('delete/<int:id>', delete_task, name='delete_task'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-task/', create_task, name='create_task'),
    path('about/', show_about, name='show_about')
]