import sqlite3
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import render
from json import dumps, load, loads

# Create your views here.
def index(request):
	return render(request, 'index.html')
	
def characters(request):
	return render(request, 'characters.html')
	
def about(request):
	return render(request, 'about.html')

def videogame(request):
	return render(request, 'videogame.html')
	
def play(request):
	return render(request, 'play.html')

