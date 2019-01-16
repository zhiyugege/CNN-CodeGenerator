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

# def getInitCode(NodeInfo, NodeGraph):

# 	channels = dict()  #通道字典
# 	re_adjacent = NodeGraph.re_adj_list #结点逆邻接表
# 	adjacent = NodeGraph.adj_list
	
# 	code = torch.torch(NodeInfo['0']) #channels
# 	channels['0'] = CreateChannel(NodeInfo['0'],NodeInfo['0'])
# 	RecurrenceCreate('0', code, channels, re_adjacent, adjacent, NodeInfo)


# def RecurrenceCreate(key, code, channels, re_adjacent, adjacent, NodeInfo):
# 	adjNode = adjacent[key]
# 	for node in adjNode:
# 		#被指向结点
# 		PointedNode = re_adjacent[node]
# 		channels_key = channels.keys()
# 		if set(channels_key)>=set(PointedNode):
# 			ChangeCode(node, channels, re_adjacent, NodeInfo)


# def ChangeCode(key, channels, re_adjacent, NodeInfo):
# 	_type = NodeInfo[key].split('-')[0]
# 	value = NodeInfo[key].split('-')[1]
# 	if _type=='1':
# 		# print(channels)
# 		# print(re_adjacent[key][0])
# 		in_channel = 0
# 		for node in re_adjacent[key]:
# 			in_channel += int(channels[node]['out'])

# 		in_channel = str(in_channel)
# 		out_channel = value.split('.')[0]
# 		width = value.split('.')[1]
# 		height = value.split('.')[2]
# 		stride = value.split('.')[3]
# 		padding = value.split('.')[4]
# 		if width==height:
# 			kernel_size = width
# 		else:
# 			kernel_size = '('+width+','+height+')'
# 		code.Conv2d(in_channel, out_channel, kernel_size, stride, padding)
# 		channels[key] = CreateChannel(in_channel, out_channel) #更新当前结点的输入输出channel


# def CreateChannel(in_channel,out_channel):
# 	channel = dict()
# 	channel['in'] = in_channel
# 	channel['out'] = out_channel
# 	return channel

