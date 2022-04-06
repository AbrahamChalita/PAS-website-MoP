import sqlite3
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from json import dumps, load, loads
import json
from random import randrange

# Create your views here.
def index(request):
	return render(request, 'index.html')
	
def characters(request):
	return render(request, 'characters.html')
	
def about(request):
	return render(request, 'about.html')

def videogame(request):
	h_var = 'Country'
	v_var = 'Friends'

	mydb = sqlite3.connect("db.sqlite3")
	curr = mydb.cursor()
	query_countries ='''SELECT Country, COUNT(Country)
		FROM User
		GROUP BY Country
	'''
	rows = curr.execute(query_countries)
	
	data = [[h_var, v_var]]

	for r in rows:
		data.append([r[0], r[1]])

	h_var_JSON = dumps(h_var)
	v_var_JSON = dumps(v_var)
	modified_data = dumps(data)

	quizId = "Quiz ID"
	Score = "Score"
	UserId = "User ID"
	Username = "Username"
	country = "Country"

	query_leaderboard ='''SELECT QuizGame.QuizID, QuizGame.Score, GameResume.UserID, 
		(SELECT country from User where UserID = GameResume.UserID),
		(SELECT username from User where UserID = GameResume.UserID) from QuizGame
		INNER JOIN GameResume on QuizGame.GameID = GameResume.GameID 
		ORDER by Score DESC
	'''
	
	rows2 = curr.execute(query_leaderboard)
	data_leaderboard = [[quizId, Score, UserId, Username, country]]

	for x in rows2:
		data_leaderboard.append([x[0], x[1], x[2], x[3], x[4]])

	leaders_data = json.dumps(data_leaderboard)
	return render(request,'videogame.html',{'values':modified_data,'h_title':h_var_JSON,'v_title':v_var_JSON, 'values2': leaders_data})
	#return render(request, 'videogame.html')
	
def play(request):
	return render(request, 'play.html')


