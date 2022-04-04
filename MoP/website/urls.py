from sys import path_hooks
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('characters/', views.characters, name='characters'),
	path('about/', views.about, name='about'),
	path('videogame/', views.videogame, name='videogame'),
	path('play/', views.play, name='play'),
]