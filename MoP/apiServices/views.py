import sqlite3
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from json import dumps, load, loads

# Create your views here.
def index(request):
	return HttpResponse("<h1>Hola desde Django!</h1>")

# user_info GET message
# Gives a json file with UserID, Username, HashPwd, Country & Name of a user
# Needs following format  =>  ?UserID=X
def user_info(request):
	query = request.GET['UserID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''SELECT UserID, Username, HashPwd, Country, Name FROM User WHERE UserID = ?'''
	rows = cur.execute(stringSQL,(query,))
	r = rows.fetchone()
		
	lista_salida = []

	if r == None:
		raise Http404("User does not exist")
	else:
		d = {}
		d["UserID"] = r[0]
		d["Username"] = r[1]
		d["HashPwd"] = r[2]	
		d["Country"] = r[3]	
		d["Name"] = r[4]
		lista_salida.append(d)
		j = dumps(lista_salida)
		return HttpResponse(j, content_type="text/json-comment-filtered")

# quiz_info GET message
# Gives a json file with UserID, Username, HashPwd, Country & Name of a user
# Needs following format  =>  ?UserID=X
def quiz_info(request):
	query = request.GET['UserID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''
	SELECT QuestionID, QuestionTxt, TimesFailed, TimesCorrect
	FROM Question 
	WHERE QuestionID IN
	(
		SELECT QuestionID 
		FROM QuestionGame 
		WHERE GameID =
		(
			SELECT GameID 
			FROM GameResume 
			WHERE UserID = ?
		)
	)'''
	rows = cur.execute(stringSQL,(query,))
	r = rows.fetchone()
		
	lista_salida = []

	if r == None:
		raise Http404("User does not exist")
	else:
		# Agregando primer resultado de querry
		d = {}
		d["QuestionID"] = r[0]
		d["QuestionTxt"] = r[1]
		d["TimesFailed"] = r[2]	
		d["TimesCorrect"] = r[3]
		lista_salida.append(d)
		# Agregando demas resultados de quesrry si existen
		for r in rows:
			d = {}
			d["QuestionID"] = r[0]
			d["QuestionTxt"] = r[1]
			d["TimesFailed"] = r[2]	
			d["TimesCorrect"] = r[3]
			lista_salida.append(d)
			
		j = dumps(lista_salida)
		return HttpResponse(j, content_type="text/json-comment-filtered")
