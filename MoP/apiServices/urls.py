from sys import path_hooks
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('user_info', views.user_info, name='user_info'),
	path('quiz_info', views.quiz_info, name='quiz_info'),
]