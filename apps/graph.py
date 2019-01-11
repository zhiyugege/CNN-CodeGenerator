class graph:
	
	#初始化
	def __init__(self,data):
		self.data = data
		self.split_data = []#[['lzy', 'big'], ['cyl', 'small'], ['lzy', 'notgood'], ['lzy', 'fat'], ['cyl', 'slim'], ['lzy', 'black'], ['cyl', 'white']]
		self.node_list = []
		self.adj_list = {}
		self.re_adj_list = {}
		self.visited = {}
		self.bfs_list = []
		self.dfs_list = []

	#分割数据
	def spilt(self):
		for couple in self.data:
			self.split_data.append(couple.split('-'))
		#print('split_data \n',self.split_data)

	#构建邻接表
	def create_adj(self):
		for couple in self.split_data:
			if self.adj_list and (couple[0] in self.adj_list):
				self.adj_list[couple[0]].append(couple[1])
			else:
			    self.adj_list.setdefault(couple[0],[]).append(couple[1])
		#print('adj_list\n ',self.adj_list)

	#构建逆邻接表
	def create_re_adj(self):
		for couple in self.split_data:
			if self.re_adj_list and (couple[1] in self.re_adj_list):
				self.re_adj_list[couple[1]].append(couple[0])
			else:
			    self.re_adj_list.setdefault(couple[1],[]).append(couple[0])
		#print('re_adj_list\n ',self.re_adj_list)

	#由分割数据获取节点集，去重
	def dup_remove_set(self):
	    result = set()
	    for sublist in self.split_data:
	        item = set(sublist)
	        result = result.union(item)
	    self.node_list = list(result)

	#初始化visited数组
	def init_visited(self):
		for node in self.node_list:
			self.visited[node] = 0
	
	#广度优先搜索遍历
	def BFS_Tranverse(self):
		self.init_visited()
		q = []
		for node in self.node_list:
			if self.visited[node] == 0:
				self.visited[node] = 1
				q.append(node)
				self.bfs_list.append(node)
				while q:
					front = q[0]
					q.pop(0)
					if front in self.adj_list:
						adj_node = self.adj_list[front]
						for adj in adj_node:
							if self.visited[adj] == 0:
					 			self.visited[adj] = 1
					 			q.append(adj)
					 			self.bfs_list.append(adj)	

	#深度优先递归
	def DFS(self, node):
		self.visited[node] = 1
		self.dfs_list.append(node)
		if node in self.adj_list:
			adj_node = self.adj_list[node]
			for adj in adj_node:
		 		if self.visited[adj] == 0:
		 			self.DFS(adj)

	#深度优先搜索遍历			 			
	def DFS_Tranverse(self):
		self.init_visited()
		for node in self.node_list:
			if self.visited[node] == 0:
				self.DFS(node)

	#设定第一个遍历节点
	def set_start(self,id):
		if id in self.node_list:
			self.node_list.remove(id)
			self.node_list.insert(0, id)
		else:
			print("Error!!!",id,'is not in the node_list.');

# data = ['0-1','0-2','1-3','1-4','2-3','3-4']
# id_start = '0'
# graph = graph(data)
# graph.spilt()
# graph.create_adj()
# graph.create_re_adj()
# graph.dup_remove_set()
# graph.set_start(id_start)
# graph.BFS_Tranverse()
# graph.DFS_Tranverse()

# print("graph.split_data\n",graph.split_data)
# print("graph.adj_list\n",graph.adj_list)
# print("graph.re_adj_list\n",graph.re_adj_list)
# print("graph.node_list\n",graph.node_list)
# print("graph.BFS_Tranverse\n",graph.bfs_list)
# print("graph.DFS_Tranverse\n",graph.dfs_list)

