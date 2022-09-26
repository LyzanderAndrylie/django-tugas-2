from django.urls import path
from todolist.views import register

from todolist.views import login_user

app_name = 'todolist'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
]