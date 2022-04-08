from sys import path_hooks
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
	path('', views.main, name='main'),
	path('progress_info', views.progress_info, name='progress_info'),
]