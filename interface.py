
class VisualInterface:
	def __init__(self, canvas, graph, edge_adds, edge_deletes, n=10):
		self.canvas = canvas
		self.graph = graph
		self.edge_adds = edge_adds
		self.edge_deletes = edge_deletes
		self.i = 0
		self.n = n

	def start(self):
		self.graph.start()
		self.canvas.start()
		self.loop()

	def loop(self):
		while self.i < self.n:
			self.graph.step()
			self.canvas.step(self.graph, self.edge_adds[self.i], self.edge_deletes[self.i])
			self.i += 1
