import drawer

class VisualInterfaceFactory:
	def create(self, graph, n=10, dynamic=False, edge_adds=[], edge_deletes=[], display_mode='dynamic'):
		return VisualInterface(self.create_canvas(graph, display_mode=display_mode, steps=n, dynamic=dynamic), graph, edge_adds=edge_adds, edge_deletes=edge_deletes, n=n, dynamic=dynamic)

	def create_canvas(self, graph, display_mode, steps, dynamic=False):
		d = self.create_drawer(graph, dynamic=dynamic)
		return drawer.SubplotCanvas(d, steps//2 + (steps % 2), 2) if 'subplot' in display_mode else drawer.DynamicCanvas(d)

	def create_drawer(self, graph, dynamic=False):
		return drawer.DynamicSubscriptionDrawer(graph, dynamic=dynamic)


class VisualInterface:
	def __init__(self, canvas, graph, edge_adds=[], edge_deletes=[], n=10, dynamic=False):
		self.canvas = canvas
		self.graph = graph
		self.dynamic = dynamic
		self.edge_adds = edge_adds
		self.edge_deletes = edge_deletes
		self.i = 0
		self.n = n


	def start(self, run=lambda: 1):
		self.graph.start()
		self.canvas.start()
		self.loop(run=run)

	def loop(self, run=lambda: 1):
		run()
		while self.i < self.n:
			# propagate influences
			self.graph.step()
			run()
			if self.dynamic:
				self.graph.update(self.adds(self.i), self.deletes(self.i))
				self.canvas.step(self.graph, self.adds(self.i), self.deletes(self.i))
			# update graph structure
			else:
				self.canvas.step(self.graph, [], [])
			self.i += 1
		self.canvas.finish()

	def adds(self, i):
		return self.edge_adds[i] if len(self.edge_adds) > i else []
	def deletes(self, i):
		return self.edge_deletes[i] if len(self.edge_deletes) > i else []
