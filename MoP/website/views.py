import sqlite3
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from json import dumps, load, loads
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
	stringSQL ='''SELECT Country, COUNT(Country)
		FROM User
		GROUP BY Country
	'''
	rows = curr.execute(stringSQL)
	
	countries = []
	players = []
	data = [[h_var, v_var]]

	for r in rows:
		countries.append(r[0])
		players.append(r[1])
		data.append([r[0], r[1]])



	h_var_JSON = dumps(h_var)
	v_var_JSON = dumps(v_var)
	modified_data = dumps(data)
	return render(request,'videogame.html',{'values':modified_data,'h_title':h_var_JSON,'v_title':v_var_JSON})
	#return render(request, 'videogame.html')
	
def play(request):
	return render(request, 'play.html')


