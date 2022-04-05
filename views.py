import re
import sqlite3
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from json import dumps, load, loads
import json

# Create your views here.
def main(request):
	return render(request, 'main.html')

#SERVICIO DE USUARIOS
#Lista DEBUG
@csrf_exempt
def GameResumeList(request):
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	string_SQL = "SELECT GameID, UserID, Difficulty, Checkpoint, DateCreate, Seconds FROM GameResume"
	rows = cur.execute(string_SQL)
	listaSalida = []

	for r in rows:
		d ={}
		d['GameID'] = r[0]
		d['UserID'] = r[1]
		d['Difficulty'] = r[2]
		d['Checkpoint'] = r[3]
		d['DateCraete'] = r[4]
		d['Secconds'] = r[5]
		listaSalida.append(d)
	
	j = dumps(listaSalida)
	return HttpResponse(j, content_type="text/json-comment-filtered")

#Servicio
@csrf_exempt
def GameResumesUser(request):
    usuario = request.GET['UserID']
    mydb = sqlite3.connect("db.sqlite3")
    cur = mydb.cursor()
    stringSQL = '''SELECT GameID FROM GameResume WHERE UserID=? '''

    rows = cur.execute(stringSQL, (str(usuario), ))
    rr = rows.fetchone()
    rows = cur.execute(stringSQL, (str(usuario), ))
    if rr == None:
        raise Http404("No existe papa")
    else:
        gamesList = []
        for r in rows:
            gamesList.append(r[0])
    
    d = {}
    d["gameIds"] = gamesList
    j = json.dumps(d)

    return HttpResponse(j, content_type="text/json-comment-filtered")