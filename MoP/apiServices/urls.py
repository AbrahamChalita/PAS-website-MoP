from sys import path_hooks
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
	path('', views.main, name='main'),
	path('progress_info', views.progress_info, name='progress_info'),
    path('unity2', views.unity2, name='unity2'),
    path('unity3', views.unity3, name='unity3'),
	path('user_info', views.user_info, name='user_info'),
	path('quiz_info', views.quiz_info, name='quiz_info'),
	path('get_games', views.get_games, name='get_games'),
	path('get_quiz_data', views.get_quiz_data, name='get_quiz_data'),
	path('quiz_request', views.quiz_request, name='quiz_request'),
	path('save_quiz', views.save_quiz, name='save_quiz'),
	path('save_level', views.save_level, name='save_level'),
	path('change_userName', views.change_userName, name='change_userName'),
	path('new_game', views.new_game, name='new_game'),
	path('instrument_stats', views.instrument_stats, name='instrument_stats'),
	path('GameResumeList', views.GameResumeList, name='GameResumeList'),
	path('GameResumesUser', views.GameResumesUser, name='GameResumesUser'),
	path('quizes_played', views.quizes_played, name='quizes_played'),
	path('score_by_quiz', views.score_by_quiz, name='score_by_quiz'),
]
