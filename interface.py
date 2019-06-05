
class VisualInterface:
	def __init__(self, canvas, dynamic_graph, edge_adds, edge_deletes, n=10):
		self.canvas = canvas
		self.dynamic_graph = dynamic_graph
		self.edge_adds = edge_adds
		self.edge_deletes = edge_deletes
		self.i = 0
		self.n = n

	def start(self):
		self.dynamic_graph.start()
		self.canvas.start()
		self.loop()

	def loop(self):
		while self.i < self.n:
			self.dynamic_graph.step(self.adds(self.i), self.deletes(self.i))
			self.canvas.step(self.dynamic_graph, self.adds(self.i), self.deletes(self.i))
			self.i += 1

	def adds(self, i):
		return self.edge_adds[i] if len(self.edge_adds) > i else []
	def deletes(self, i):
		return self.edge_deletes[i] if len(self.edge_deletes) > i else []
