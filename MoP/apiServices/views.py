import re
import sqlite3
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from json import dumps, load, loads

# Create your views here.
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