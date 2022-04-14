from sys import path_hooks
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
	path('', views.main, name='main'),
    path('unity2', views.unity2, name='unity2'),
    path('unity3', views.unity3, name='unity3'),
	path('user_info', views.user_info, name='user_info'),
	path('quiz_info', views.quiz_info, name='quiz_info'),
	path('get_games', views.get_games, name='get_games'),
	path('get_quiz_data', views.get_quiz_data, name='get_quiz_data'),
	path('quiz_request', views.quiz_request, name='quiz_request'),
]