from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import render

def index(request):
	
	return render(request, 'index.html')