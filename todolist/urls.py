from django.urls import path
from todolist.views import delete_task, register

from todolist.views import login_user
from todolist.views import logout_user

from todolist.views import show_todolist
from todolist.views import create_task
from todolist.views import update_task
from todolist.views import delete_task

app_name = 'todolist'

urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('update/<int:id>', update_task, name='update_task'),
    path('delete/<int:id>', delete_task, name='delete_task'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-task', create_task, name='create_task')
]