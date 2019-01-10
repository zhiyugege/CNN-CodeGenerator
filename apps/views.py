from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import render

def index(request):
	
	return render(request, 'index.html')

def GenerateApi(request):

	NodeInfo = request.POST.get('NodeInfo')
	LineInfo = request.POST.getlist('LineInfo')

	NodeInfo = eval(NodeInfo)
	print(NodeInfo, LineInfo);
	context = {'back':'ok'}
	return  JsonResponse(context)
	