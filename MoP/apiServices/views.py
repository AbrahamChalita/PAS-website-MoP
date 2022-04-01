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
# def user_info(request):
# 	query = request.GET['UserID']
# 	mydb = sqlite3.connect("db.sqlite3")
# 	cur = mydb.cursor()
# 	stringSQL = '''SELECT UserID, Username, HashPwd, Country, Name FROM User WHERE UserID = ?'''
# 	rows = cur.execute(stringSQL,(query,))
# 	r = rows.fetchone()
		
# 	lista_salida = []

# 	if r == None:
# 		raise Http404("User does not exist")
# 	else:
# 		d = {}
# 		d["UserID"] = r[0]
# 		d["Username"] = r[1]
# 		d["HashPwd"] = r[2]	
# 		d["Country"] = r[3]	
# 		d["Name"] = r[4]
# 		return JsonResponse(d)

def user_info(request):
	query = request.GET['UserID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''SELECT Username, UserID, HashPwd, Country FROM User WHERE UserID = ?'''
	rows = cur.execute(stringSQL,(query,))
	r = rows.fetchone()
		
	lista_salida = []

	if r == None:
		raise Http404("User does not exist")
	else:
		d = {}
		d["userName"] = r[0]
		d["id"] = r[1]
		d["pwd"] = r[2]	
		d["country"] = r[3]
		return JsonResponse(d)

# quiz_info GET message
# Gives a json file with UserID, Username, HashPwd, Country & Name of a user
# Needs following format  =>  ?UserID=X
def quiz_info(request):
	query = request.GET['UserID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	# Querry de acceso a datos
	stringSQL = '''
	SELECT QuestionID, QuestionTxt, TimesFailed, TimesCorrect
	FROM Question 
	WHERE QuestionID IN
	(
		SELECT QuestionID 
		FROM QuestionGame 
		WHERE GameID IN
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
		raise Http404("User has not played any quizes.")
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
		
# get_quiz_data GET
# 
def get_quiz_data(request):
	query = request.GET['UserID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	# Querry de acceso a datos
	stringSQL = '''
	SELECT QuestionID, Correct
  	FROM QuestionGame
	WHERE QuizID IN (
		SELECT QuizID
		FROM QuestionGame
		WHERE GameID IN (
			SELECT GameID
			FROM GameResume
			WHERE UserID = ?
		)
 	)'''
	rows = cur.execute(stringSQL,(query,))
	lista_salida = []
	r = rows.fetchone()

	if r == None:
		raise Http404("User does not have any saved games")
	else:
		d = {}
		d["QuestionID"] = r[0]
		d["Correct"] = r[1]
		lista_salida.append(d)
		for r in rows:
			d = {}
			d["QuestionID"] = r[0]
			d["Correct"] = r[1]
			lista_salida.append(d)
			
		j = dumps(lista_salida)
		return HttpResponse(j, content_type="text/json-comment-filtered")

# get_games GET message
# Gives a json file with all the GameResume objects GameID, UserId, Difficulty, Checkpoint, DateCreated and Seconds
def get_games(request):
	query = request.GET['UserID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	# Querry de acceso a datos
	stringSQL = '''
	SELECT GameID, Difficulty, Checkpoint, DateCreate, Seconds 
	FROM GameResume 
	WHERE UserID = ?'''
	# Send query
	rows = cur.execute(stringSQL,(query,))
	r = rows.fetchone()

	lista_salida = []
	# Empty result
	if r == None:
		raise Http404("User does not have any saved games")
	# Reading result
	else:
		# First result data
		d = {}
		d["QuestionID"] = r[0]
		d["QuestionTxt"] = r[1]
		d["TimesFailed"] = r[2]	
		d["TimesCorrect"] = r[3]
		lista_salida.append(d)
		# Data from next results
		for r in rows:
			d = {}
			d["QuestionID"] = r[0]
			d["QuestionTxt"] = r[1]
			d["TimesFailed"] = r[2]	
			d["TimesCorrect"] = r[3]
			lista_salida.append(d)
		# Parse to JSON
		j = dumps(lista_salida)
		return HttpResponse(j, content_type="text/json-comment-filtered")