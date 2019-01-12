import os
import sys
from django.http import HttpResponse, Http404, StreamingHttpResponse
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import render
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
	
	context = {'back':'ok'}
	return  JsonResponse(context)
	

def getNodeGraph(NodeInfo, LineInfo):

	g = graph.graph(LineInfo)
	g.spilt()
	g.create_adj()
	g.create_re_adj()
	return g

def downloadApi(request):

	path = sys.path[0]
	file = open(path+'\\static\\hello.txt','r')
	download_file='django.py'
	response=StreamingHttpResponse(file)
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(download_file)
	return response
	# print("graph.adj_list\n",g.adj_list)
	# print("graph.re_adj_list\n",g.re_adj_list)



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

