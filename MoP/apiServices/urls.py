from sys import path_hooks
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
	path('', views.main, name='main'),
	path('user_info', views.user_info, name='user_info'),

    path('unity2', views.unity2, name='unity2'), # Login
    path('unity3', views.unity3, name='unity3'), # Registro
	path('change_userName', views.change_userName, name='change_userName'), # Cambiar nombre de usuario
	path('new_game', views.new_game, name='new_game'), # Crea nueva partida
	path('get_games', views.get_games, name='get_games'), # Partidas del usuario
	path('update_checkpoint', views.update_checkpoint, name='update_checkpoint'), # Actualiza checkpoint al entrar a un hubworld

	path('save_level', views.save_level, name='save_level'), # Guarda datos de nivel de plataforma
	
	path('quiz_request', views.quiz_request, name='quiz_request'), # Recupera preguntas y respuestas
	path('save_quiz', views.save_quiz, name='save_quiz'), # Guarda datos del quiz

	path('quizes_played', views.quizes_played, name='quizes_played'), # Quizes jugados por el usuario
	path('score_by_quiz', views.score_by_quiz, name='score_by_quiz'), # Scores del jugador por quiz
	path('hardest_question', views.hardest_question, name='hardest_question'), # Scores del jugador por quiz
	path('update_seconds', views.update_seconds, name='update_seconds'), # Scores del jugador por quiz
	path('seconds_played', views.seconds_played, name='seconds_played'), # Scores del jugador por quiz

	path('progress_info', views.progress_info, name='progress_info'),
	path('quiz_info', views.quiz_info, name='quiz_info'),
	path('get_quiz_data', views.get_quiz_data, name='get_quiz_data'),
	path('instrument_stats', views.instrument_stats, name='instrument_stats'),
	path('GameResumeList', views.GameResumeList, name='GameResumeList'),
	path('GameResumesUser', views.GameResumesUser, name='GameResumesUser'),
]
