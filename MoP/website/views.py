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
    # here starts the code for world stats
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

	# here starts the code for leaderboard

	query_leaderboard ='''SELECT QuizGame.QuizID, QuizGame.Score, 
		(SELECT country from User where UserID = GameResume.UserID),
		(SELECT username from User where UserID = GameResume.UserID) from QuizGame
		INNER JOIN GameResume on QuizGame.GameID = GameResume.GameID 
		ORDER by Score DESC
	'''
	
	rows2 = curr.execute(query_leaderboard)
	data_leaderboard = []

	counter = 0
	for x in rows2:
			counter += 1
			data_leaderboard.append([counter, x[0], x[1], x[2], x[3]])

	# Here starts code for player count stats
	query_totalplayers ='''SELECT (
		SELECT COUNT (DISTINCT UserID) from GameResume) 
		as total_players, 
		(SELECT SUM(Seconds) as total_playtime from GameResume) 
		as total_playtime
	'''
	v_player = "Players"
	v_numbers = "Total"
	rows3 = curr.execute(query_totalplayers)
	data_players = [[v_player, v_numbers]]
	data_total = 0
 
	for y in rows3:
			data_players.append(["Players", y[0],])
			data_total = y[0]
	
	modified_players = dumps(data_players)
		
	return render(request,'videogame.html',{'values':modified_data,'h_title':h_var_JSON,'v_title':v_var_JSON, 'values2': data_leaderboard, 'values3': modified_players, 'values4': data_total})
	#return render(request, 'videogame.html')
	
def play(request):
	return render(request, 'play.html')


