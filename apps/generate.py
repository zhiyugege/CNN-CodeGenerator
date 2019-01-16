class generate:

	def __init__(self, NodeInfo, NodeGraph, code):
		self.NodeInfo = NodeInfo
		self.NodeGraph = NodeGraph
		self.channels = dict()
		self.result = dict()
		self.re_adjacent = NodeGraph.re_adj_list #结点逆邻接表
		self.adjacent = NodeGraph.adj_list
		self.code = code
		self.channels['0'] = self.CreateChannel(NodeInfo['0'],NodeInfo['0'])
		self.result['0'] = 'input'
		self.outputs = ''

	def RecurrenceCreate(self, key):
		if key in self.adjacent.keys():
			adjNode = self.adjacent[key]
			for node in adjNode:
				#被指向结点
				PointedNode = self.re_adjacent[node]
				channels_key = self.channels.keys()
				if set(channels_key)>=set(PointedNode):
					self.ChangeCode(node,PointedNode)
					self.RecurrenceCreate(node)

	def ChangeCode(self,key,PointedNode):
		_type = self.NodeInfo[key].split('-')[0]
		value = self.NodeInfo[key].split('-')[1]
		if _type=='1':

			in_channel = 0
			for node in self.re_adjacent[key]:
				in_channel += int(self.channels[node]['out'])
			in_channel = str(in_channel)

			out_channel = value.split('.')[0]
			width = value.split('.')[1]
			height = value.split('.')[2]
			stride = value.split('.')[3]
			padding = value.split('.')[4]
			if width==height:
				kernel_size = width
			else:
				kernel_size = '('+width+','+height+')'
			inputs = self.result[PointedNode[0]]
			outputs = self.code.Conv2d(in_channel, out_channel, kernel_size, stride, padding, inputs)
			self.outputs = outputs
			self.channels[key] = self.CreateChannel(in_channel, out_channel) #更新当前结点的输入输出channel
			self.result[key] = outputs

		elif _type =='2':

			sign = value.split('.')[0]
			kernel_size = value.split('.')[1]
			stride = value.split('.')[2]

			in_channel = 0
			for node in self.re_adjacent[key]:
				in_channel += int(self.channels[node]['out'])
			in_channel = str(in_channel)
			out_channel = in_channel
			inputs = self.result[PointedNode[0]]
			outputs = self.code.Pool2d(sign, kernel_size, stride, inputs)
			self.outputs = outputs
			self.channels[key] = self.CreateChannel(in_channel, out_channel)
			self.result[key] = outputs

		elif _type =='3':

			in_channel = 0
			for node in self.re_adjacent[key]:
				in_channel += int(self.channels[node]['out'])
			in_channel = str(in_channel)
			out_channel = in_channel
			inputs = self.result[PointedNode[0]]
			outputs = self.code.BatchNorm(in_channel, inputs)
			self.outputs = outputs
			self.channels[key] = self.CreateChannel(in_channel, out_channel)
			self.result[key] = outputs

		elif _type =='4':
			in_channel = 0
			for node in self.re_adjacent[key]:
				in_channel += int(self.channels[node]['out'])
			in_channel = str(in_channel)
			out_channel = in_channel
			inputs = self.result[PointedNode[0]]
			outputs = self.code.Activations(value, inputs)
			self.outputs = outputs
			self.channels[key] = self.CreateChannel(in_channel, out_channel)
			self.result[key] = outputs

		elif _type =='5':
			in_channel = 0
			for node in self.re_adjacent[key]:
				in_channel += int(self.channels[node]['out'])
			in_channel = str(in_channel)
			out_channel = value
			inputs = self.result[PointedNode[0]]
			outputs = self.code.Fc(in_channel, out_channel, inputs)
			self.outputs = outputs
			self.channels[key] = self.CreateChannel(in_channel, out_channel)
			self.result[key] = outputs

		elif _type =='6':
			in_channel = 0
			inputs = []
			outputs = '0'
			for node in self.re_adjacent[key]:
				in_channel += int(self.channels[node]['out'])
			in_channel = str(in_channel)
			out_channel = in_channel
			for node in PointedNode:
				inputs.append(self.result[node])
			if len(inputs):
				outputs = self.code.Concat(inputs,value)
				self.outputs = outputs
			self.channels[key] = self.CreateChannel(in_channel, out_channel)
			self.result[key] = outputs
			
	def CreateChannel(self, in_channel, out_channel):
		channel = dict()
		channel['in'] = in_channel
		channel['out'] = out_channel
		return channel

	def getReturnCode(self):
		self.code.Return(self.outputs)