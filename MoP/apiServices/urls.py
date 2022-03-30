from sys import path_hooks
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
]