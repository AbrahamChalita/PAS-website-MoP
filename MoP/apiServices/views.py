import re
import sqlite3
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from json import dumps, load, loads

# Create your views here.
def main(request):
	return render(request, 'main.html')

# Gives json file with overall player count and overall playedtime api/totalplayers_stats
def totalplayers_stats(request):
	mydb = sqlite3.connect("db.sqlite3")
	curr = mydb.cursor()
	stringSQL = '''SELECT (
		SELECT COUNT (DISTINCT UserID) from GameResume) 
		as total_players, 
		(SELECT SUM(Seconds) as total_playtime from GameResume) 
		as total_playtime
	'''
	rows = curr.execute(stringSQL)
	listaSalida = []

	for r in rows:
		d = {}
		d['TotalPlayers'] = r[0]
		d['TotalPlayTime'] = r[1]
		listaSalida.append(d)
	
	j = dumps(listaSalida)
	return HttpResponse(j, content_type="text/json-comment-filtered")

# Gives json file with information to construct leaderboard api/leaderboard_stats
def leaderboard_stats(request):
	mydb = sqlite3.connect("db.sqlite3")
	curr = mydb.cursor()
	stringSQL ='''SELECT QuizGame.QuizID, QuizGame.Score, GameResume.UserID, 
		(SELECT country from User where UserID = GameResume.UserID),
		(SELECT username from User where UserID = GameResume.UserID) from QuizGame
		INNER JOIN GameResume on QuizGame.GameID = GameResume.GameID 
		ORDER by Score DESC
	'''
	rows = curr.execute(stringSQL)
	listaSalida = []

	for r in rows:
		d = {}
		d['QuizId'] = r[0]
		d['Score'] = r[1]
		d['UserId'] = r[2]
		d['Username'] = r[3]
		d['Country'] = r[4]
		listaSalida.append(d)
	
	j = dumps(listaSalida)
	return HttpResponse(j, content_type="text/json-comment-filtered")

# Gives json file most used instrument api/instrument_stats
def instrument_stats(request):
	mydb = sqlite3.connect("db.sqlite3")
	curr = mydb.cursor()
	stringSQL ='''SELECT  UserInstrument.DmgDone, UserInstrument.Playtime, Instrument.Description,
		(SELECT username from User where UserID = UserInstrument.UserID) 
		from Instrument
		INNER JOIN UserInstrument on UserInstrument.InstrumentID = Instrument.InstrumentID 
		ORDER BY DmgDone DESC
	'''
	rows = curr.execute(stringSQL)
	listaSalida = []

	for r in rows:
		d = {}
		d['DamageDone'] = r[0]
		d['Playtime'] = r[1]
		d['Description'] = r[2]
		d['Username'] = r[3]
		listaSalida.append(d)
	
	j = dumps(listaSalida)
	return HttpResponse(j, content_type="text/json-comment-filtered")
