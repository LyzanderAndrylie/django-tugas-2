from django.urls import path
from todolist.views import register

app_name = 'todolist'

urlpatterns = [
    path('register/', register, name='register'),
]