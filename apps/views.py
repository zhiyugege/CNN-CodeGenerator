import os
import sys
from django.http import HttpResponse, Http404, StreamingHttpResponse
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from . import graph
from . import torch
from . import generate
def index(request):
	
	return render(request, 'index.html')

def GenerateApi(request):

	NodeInfo = request.POST.get('NodeInfo')
	LineInfo = request.POST.getlist('LineInfo')
	NodeInfo = eval(NodeInfo)

	NodeGraph = getNodeGraph(NodeInfo,LineInfo)
	code = torch.torch(NodeInfo['0'])

	Generator = generate.generate(NodeInfo, NodeGraph, code)                                         	
	Generator.RecurrenceCreate('0')
	Generator.getReturnCode()
	init_code = Generator.code.code
	forward_code = Generator.code.forward

	context = {'status':'ok','init_code':init_code,'forward':forward_code}
	return  JsonResponse(context)
	
	

def getNodeGraph(NodeInfo, LineInfo):

	g = graph.graph(LineInfo)
	g.spilt()
	g.create_adj()
	g.create_re_adj()
	return g

def downloadApi(request):

	init_code = request.POST.get('init_code')
	forward_code = request.POST.get('forward_code')
	the_file_name = request.POST.get('panel_name')+'.py'
	init_code = init_code.split('$')
	forward_code = forward_code.split('$')
	print(init_code,forward_code)
	path = sys.path[0]

	with open(path+'\\static\\hello.txt','w') as w:
		w = writeCode(init_code, w)
		w = writeCode(forward_code, w)
	def file_iterator(file_name, chunk_size=512):
		with open(path+'\\static\\hello.txt','r') as f:
			while True:
				c = f.read(chunk_size)
				if c:
					yield c
				else:
					break
 
	# the_file_name = name
	response = StreamingHttpResponse(file_iterator(the_file_name))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
	return response


def writeCode(code, file):
	for i in range(len(code)):
		if code[i]!='':
			if code[i][:3]=='imp' or code[i][:3]=='fro' or code[i][:3]=='cla':
				file.write(code[i]+'\n')
			elif code[i][:3]=='def':
				file.write('	'+code[i]+'\n')
			else:
				file.write('		'+code[i]+'\n')	
	return file


