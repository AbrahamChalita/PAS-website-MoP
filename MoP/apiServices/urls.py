from sys import path_hooks
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
	path('', views.main, name='main'),
	path('totalplayers_stats', views.totalplayers_stats, name='totalplayers_stats'),
	path('leaderboard_stats', views.leaderboard_stats, name='leaderboard_stats'),
	path('instrument_stats', views.instrument_stats, name='instrument_stats'),
]