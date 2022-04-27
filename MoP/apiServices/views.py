import re
import sqlite3
import string
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from json import dumps, load, loads
from django.views.decorators.csrf import csrf_exempt
import json

################
# GET Messages #
################

def main(request):
	return render(request, 'main.html')

def progress_info(request):
	query = request.GET['UserID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()

	# acceso a los datos a traves del query 
	stringSQL = '''
		SELECT Correct  as  value from QuestionGame where QuizPlayID in 
		(SELECT QuizPlayID from QuizGame where GameID in
		(SELECT GameID from GameResume where UserID = ?))
	'''

	rows = cur.execute(stringSQL,(query,))
	r = rows.fetchone()

	lista_salida = []

	good = 0
	bad = 0
	count = 0
	
	if r == None:
		raise Http404("User does not have any saved games")
	else:
		count += 1
		if (r[0] == 1):
			good += 1
		else:
			bad += 1
		for r in rows:
			count += 1
			if (r[0] == 1):
				good += 1
			else:
				bad += 1

		
		d = {}
		d["Good answers percentage"] = (f"{good/count * 100} %")
		d["Bad answers percentage"] = (f"{bad/count * 100} %")
		lista_salida.append(d)
		j = dumps(lista_salida)
		return HttpResponse(j, content_type="text/json-comment-filtered")

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
		d["gameID"] = r[0]
		d["difficulty"] = r[1]
		d["checkpoint"] = r[2]
		d["dateCreate"] = r[3]
		d["seconds"] = r[4]
		# d2 = {}
		# d2['GameResume'] = d
		lista_salida.append(d)
		# Data from next results
		for r in rows:
			d = {}
			d["gameID"] = r[0]
			d["difficulty"] = r[1]
			d["checkpoint"] = r[2]
			d["dateCreate"] = r[3]
			d["seconds"] = r[4]
			# d2 = {}
			# d2['GameResume'] = d
			lista_salida.append(d)

		d3 = {}
		d3['games'] = lista_salida
		# Parse to JSON
		j = dumps(d3)
		return HttpResponse(j, content_type="text/json-comment-filtered")

# get_quiz_data GET
# Obtiene todos los datos de 
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

def quiz_request(request):
	query = request.GET['QuizID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''
	SELECT QuestionTxt, QuestionID
	FROM Question
	WHERE QuizID = ?
	'''
	questions = cur.execute(stringSQL,(query,))
	
	questionArr = []
	for question in questions:
		d = {}
		d["questionID"] = question[1]
		d["questionTxt"] = question[0]
		d["options"] =  question[1]
		questionArr.append(d)
	
	for question in questionArr:
		stringSQL = '''
		SELECT OptionTxt, Correct
		FROM QuestionOptions
		WHERE QuestionID = ?
		'''
		options = cur.execute(stringSQL,(question['options'],))
		optionArr = []
		for option in options:
			d2 = {}
			d2["optionTxt"] = option[0]
			d2["correct"] = option[1]
			optionArr.append(d2)
		question['options'] = optionArr

	res = {}
	res['quiz'] = questionArr

	j = dumps(res)
	return HttpResponse(j, content_type="text/json-comment-filtered")

def quizes_played(request):
	query = request.GET['UserID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()

	stringSQL = '''
	SELECT QuizID
	FROM QuizGame
	WHERE GameID IN
	(
		SELECT GameID
		FROM GameResume
		WHERE UserID = ?
	)
	GROUP BY QuizID
	'''

	rows = cur.execute(stringSQL,(query,))
	r = rows.fetchone()
		
	lista_salida = []
	d = {}

	if r == None:
		raise Http404("User has not played any quizes.")
	else:
		# Agregando primer resultado de querry
		lista_salida.append(r[0])
		# Agregando demas resultados de quesrry si existen
		for r in rows:
			lista_salida.append(r[0])

	d['quizes'] = lista_salida

	j = dumps(d)
	return HttpResponse(j, content_type="text/json-comment-filtered")

def hardest_question(request):
	query = request.GET['UserID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()

	stringSQL = '''
	SELECT QuestionTxt
	FROM Question
	WHERE QuestionID IN
	(
		SELECT QuestionID
		FROM QuestionGame
		WHERE QuizPlayID IN
		(
			SELECT QuizPlayID
			FROM QuizGame
			WHERE GameID IN 
			(
				SELECT GameID
				FROM GameResume
				WHERE UserID = ?
			)
		)
		GROUP By QuestionID
		ORDER By sum(Correct) ASC
		LIMIT 1
	)
	'''

	rows = cur.execute(stringSQL,(query,))
	r = rows.fetchone()

	d = {}

	if r == None:
		raise Http404("User has not played any quizes.")
	else:
		d['question'] = r[0]

	j = dumps(d)
	return HttpResponse(j, content_type="text/json-comment-filtered")

def update_seconds(request):
	query = request.GET['GameID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()

	stringSQL = '''
	SELECT Seconds
	FROM GameResume
	WHERE GameID = ?
	'''

	rows = cur.execute(stringSQL,(query,))
	seconds = rows.fetchone()[0]

	stringSQL = '''
	SELECT Seconds
	FROM GameResume
	WHERE GameID = ?
	'''

	seconds = seconds + int(request.GET['Seconds'])

	stringSQL = '''
	UPDATE GameResume
	SET Seconds = ?
	WHERE GameID = ?
	'''
	
	mydb.commit()
	mydb.close()

	rows = cur.execute(stringSQL,(seconds,query,))

	d = {}
	j = dumps(d)
	return HttpResponse(j, content_type="text/json-comment-filtered")

def seconds_played(request):
	query = request.GET['UserID']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()

	stringSQL = '''
	SELECT sum(Seconds)
	FROM GameResume
	WHERE UserID = ?
	'''

	rows = cur.execute(stringSQL,(query,))
	r = rows.fetchone()

	d = {}

	if r == None:
		raise Http404("User has not played any quizes.")
	else:
		d['seconds'] = r[0]

	j = dumps(d)
	return HttpResponse(j, content_type="text/json-comment-filtered")

#################
# POST Messages #
#################

@csrf_exempt
def score_by_quiz(request):
	body_unicode = request.body.decode('utf-8')
	body = loads(body_unicode)

	print(body)
	
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()

	stringSQL = '''
	SELECT Score
	FROM QuizGame
	JOIN GameResume
				On QuizGame.GameID = GameResume.GameID
	Join User
				On User.UserID = GameResume.UserID
				WHERE User.UserID = ? AND QuizGame.QuizID = ?
	'''

	rows = cur.execute(stringSQL,(body['userID'], body['quizID'],))
	r = rows.fetchone()

	lista_salida = []
	d = {}

	if r == None:
		raise Http404("User has not played any quizes.")
	else:
		# Agregando primer resultado de querry
		lista_salida.append(r[0])
		# Agregando demas resultados de quesrry si existen
		for r in rows:
			lista_salida.append(r[0])

	d['scores'] = lista_salida

	j = dumps(d)
	return HttpResponse(j, content_type="text/json-comment-filtered")

@csrf_exempt
def unity2(request):
	body_unicode = request.body.decode('utf-8')
	body = loads(body_unicode)
	print(body)
	
	query = body['userName']
	query = body['pwd']
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''
	SELECT Username, UserID, HashPwd, Country
	FROM User
	WHERE User.HashPwd = ? AND User.Username = ?
	'''
	rows = cur.execute(stringSQL,(body['pwd'],body['userName'],))
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

from datetime import datetime
@csrf_exempt
def new_game(request):
	body_unicode = request.body.decode('utf-8')
	body = loads(body_unicode) # convierte en diccionario el body del POST

	# Guardando score del QuizPlay en la base de datos
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''
	INSERT INTO GameResume (UserID, Difficulty, Checkpoint, DateCreate, Seconds) 
	VALUES (?,?,?,?,?)
	'''

	# current date and time
	timestamp = datetime.now().replace(microsecond=0).isoformat(' ')
	cur.execute(stringSQL,(body['userID'],body['difficulty'],0,timestamp,0,))

	# Obteniendo QuizPlayID del registro
	stringSQL = '''
	SELECT GameID, UserID, Difficulty, Checkpoint, DateCreate, Seconds
	FROM GameResume
	ORDER BY GameID DESC
	LIMIT 1
	'''
	gameId = cur.execute(stringSQL)
	game = gameId.fetchone()
	d = {}
	d['gameID'] = game[0]
	d['userID'] = game[1]
	d['difficulty'] = game[2]
	d['checkpoint'] = game[3]
	d['dateCreated'] = game[4]
	d['seconds'] = game[5]

	j = dumps(d)
	mydb.commit()
	mydb.close()
	return HttpResponse(j, content_type="text/json-comment-filtered")	

@csrf_exempt
def save_quiz(request):
	body_unicode = request.body.decode('utf-8')
	body = loads(body_unicode) # convierte en diccionario el body del POST

	# Guardando score del QuizPlay en la base de datos
	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''
	INSERT INTO QuizGame (QuizID, GameID, Score) 
	VALUES (?,?,?)
	'''
	cur.execute(stringSQL,(body['QuizID'], body['GameID'], body['Score'],))

	# Obteniendo QuizPlayID del registro
	stringSQL = '''
	SELECT QuizPlayID
	FROM QuizGame
	ORDER BY QuizPlayID DESC
	LIMIT 1
	'''
	quizPlayId = cur.execute(stringSQL)
	d = {}
	d['QuizPlayID'] = quizPlayId.fetchone()[0]

	# Guardando respuesta a cada pregunta en la base de datos
	stringSQL = '''
	INSERT INTO QuestionGame (QuizPlayID, QuestionID, Correct) 
	VALUES (?,?,?)
	'''
	for i in range(len(body['QuestionID'])):
		cur.execute(stringSQL,(d['QuizPlayID'], body['QuestionID'][i], body['Correct'][i],))

	j = dumps(d)
	mydb.commit()
	mydb.close()
	return HttpResponse(j, content_type="text/json-comment-filtered")

@csrf_exempt
def save_level(request):
	body_unicode = request.body.decode('utf-8')
	body = loads(body_unicode) # convierte en diccionario el body del POST

	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''
	INSERT INTO LevelGame (LevelID, GameID, Score, Playtime) 
	VALUES (?,?,?,?)
	'''

	cur.execute(stringSQL,(body['LevelID'], body['GameID'], body['Score'], body['Playtime'],))

	mydb.commit()
	mydb.close()
	cur = mydb.cursor()
	stringSQL = '''
	SELECT LevelPlayID
	FROM LevelGame
	ORDER BY LevelPlayID DESC
	LIMIT 1
	'''
	quizPlayId = cur.execute(stringSQL)

	d = {}
	d["LevelPlayID"] = quizPlayId.fetchone()[0]

	j = dumps(d)
	return HttpResponse(j, content_type="text/json-comment-filtered")

@csrf_exempt
def change_userName(request):
	body_unicode = request.body.decode('utf-8')
	body = loads(body_unicode) # convierte en diccionario el body del POST

	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''
	UPDATE User
	SET Username = ?
	WHERE UserID = ?
	'''

	cur.execute(stringSQL,(body['Username'], body['UserID'],))

	d = {}

	mydb.commit()
	mydb.close()
	return JsonResponse(d)

@csrf_exempt
def update_checkpoint(request):
	body_unicode = request.body.decode('utf-8')
	body = loads(body_unicode) # convierte en diccionario el body del POST

	mydb = sqlite3.connect("db.sqlite3")
	cur = mydb.cursor()
	stringSQL = '''
	UPDATE GameResume
	SET Checkpoint = ?
	WHERE GameID = ?
	'''

	cur.execute(stringSQL,(body['checkpoint'], body['gameID'],))

	d = {}

	mydb.commit()
	mydb.close()
	return JsonResponse(d)

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
