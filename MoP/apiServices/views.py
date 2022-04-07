import sqlite3
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from json import dumps, load, loads

# Create your views here.
def index(request):
	return HttpResponse("<h1>Hola desde Django!</h1>")

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

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def unity2(request):
	body_unicode = request.body.decode('utf-8')
	body = loads(body_unicode)
	print(body)
	
	query = body['userName']
	query = body['pwd']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''SELECT Username, UserID, HashPwd, Country FROM User WHERE Username = ?'''
	rows = cur.execute(stringSQL,(query,))
	r = rows.fetchone()

	if r == None:
		raise Http404("User does not exist or credentials invalid")
	else:
		d = {}
		d["userName"] = r[0]
		d["id"] = r[1]
		d["pwd"] = r[2]
		d["country"] = r[3]
		return JsonResponse(d)

# Registro de nuuevo usuario a la base de datos
@csrf_exempt
def unity3(request):
	body_unicode = request.body.decode('utf-8')
	body = loads(body_unicode) # convierte en diccionario el body del POST

	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''
	INSERT INTO User (Name, Username, HashPwd, Country, Email) 
	VALUES (?,?,?,?,?)
	'''

	cur.execute(stringSQL,(body['name'], body['userName'], body['pwd'], body['country'], body['email'],))

	mydb.commit()
	mydb.close()
	
	return unity2(request)

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
		Select QuestionID
		FROM QuestionGame
		Where QuizPlayID IN (
			SELECT QuizPlayID 
			FROM QuizGame 
			WHERE GameID IN
			(
				SELECT GameID 
				FROM GameResume 
				WHERE UserID = ?
			)
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
		d["GameID"] = r[0]
		d["Difficulty"] = r[1]
		d["Checkpoint"] = r[2]
		d["DateCreate"] = r[3]
		d["Seconds"] = r[4]
		lista_salida.append(d)
		# Data from next results
		for r in rows:
			d = {}
			d["GameID"] = r[0]
			d["Difficulty"] = r[1]
			d["Checkpoint"] = r[2]
			d["DateCreate"] = r[3]
			d["Seconds"] = r[4]
			lista_salida.append(d)
		# Parse to JSON
		j = dumps(lista_salida)
		return HttpResponse(j, content_type="text/json-comment-filtered")

# get_quiz_data GET
# 
def get_quiz_data(request):
	query = request.GET['UserID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''
	SELECT GameID
	FROM GameResume
	WHERE UserID = ?
	'''
	# Getting GameIds of user
	gameIds = cur.execute(stringSQL,(query,))
	gameArr = []

	for gameId in gameIds:
		quizArr = []
		# Creando diccionario
		dictGames = {}
		stringSQL = '''
		SELECT QuizPlayID
		FROM QuizGame 
		WHERE GameID = ?
		'''
		# Getting quizPlayIds of user
		quizPlayIds = cur.execute(stringSQL,(gameId[0],))

		for quizPlayId in quizPlayIds:
			questionArr = []
			# Creando diccionario
			dictQuizes = {}
			stringSQL = '''
			SELECT QuestionID, Correct
			FROM QuestionGame
			WHERE QuizPlayID = ?
			'''
			# Obteniendo pregunta
			questions = cur.execute(stringSQL,(quizPlayId[0],))
			for question in questions:
				dictQuestions = {}
				dictQuestions["questionID"] = question[0]
				dictQuestions["correct"] = question[1]
				questionArr.append(dictQuestions)
				print(questionArr)

			#Query para obtener 
			stringSQL = '''
			SELECT QuizID
			FROM QuizGame
			WHERE QuizPlayID = ?
			'''
			# Obteniendo pregunta
			quiz = cur.execute(stringSQL,(quizPlayId[0],))
			quizId = quiz.fetchone()

			dictQuizes["quizID"] = quizId[0]
			dictQuizes["questions"] = questionArr
			quizArr.append(dictQuizes)

		dictGames["gameID"] = gameId[0]
		dictGames["quizes"] = quizArr
		gameArr.append(dictGames)

	j = dumps(gameArr)
	return HttpResponse(j, content_type="text/json-comment-filtered")
