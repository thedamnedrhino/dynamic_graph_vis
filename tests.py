import graph
import drawer
import interface


class VisualSubscriptionTest:

	def __init__(self, test_set=0):

		self.i = test_set
		self.graph = self.create_graph()
		self.canvas = self.create_canvas(self.graph)
		self.interface = self.create_interface(self.graph, self.canvas, self.edge_adds(self.i), self.edge_deletes(self.i))

	def test(self):
		self.interface.start()
		self.interface.loop()


	def create_interface(self, graph, canvas, edge_adds, edge_deletes):
		return interface.VisualInterface(canvas, graph, edge_adds, edge_deletes)

	def create_canvas(self, graph):
		d = self.create_drawer(graph)
		return drawer.DynamicCanvas(d)

	def create_drawer(self, graph):
		return drawer.DynamicSubscriptionDrawer(graph)

	def create_graph(self):
		nodes = {l: graph.SubscriptionNode(l, threshold, lamb) for l, threshold, lamb in self.node_data()[self.i][0]}
		for n in self.node_data()[self.i][1]:
			nodes[n].activate()
		g = graph.DynamicGraph(nodes)
		for u, v in self.edge_data()[self.i][0]:
			g.add_edge(u, v)
		return g


	def node_data(self):
		"""
		return: [([nodes: (label, threshold, lambda)], [initially activated])]
		"""
		lamb = 2
		return [(
				(
			(1, 4, lamb),
			(2, 2, lamb),
			(3, 1, lamb),
			(4, 3, lamb),
				), (1,)
				)
				]
	def edge_data(self):
		"""
		coupled to node_data
		return: [([initial: (source, destination)], [adds], [deletes])]
		"""
		undirected = [(1, 2), (2, 3), (3, 1), (1, 4), (2, 4), (3, 4)]
		directed = undirected + [(v, u) for (u, v) in undirected]
		adds = [[]] * 10
		deletes = adds
		return [(directed, adds, deletes)]

	def edge_adds(self, i):
		return self.edge_data()[i][1]
	def edge_deletes(self, i):
		return self.edge_data()[i][2]

class RandomGraphVisualSubscriptionTest(VisualSubscriptionTest):
	def __init__(self):
		self.graph, (edge_adds, edge_deletes) = graph.RandomGraphGenerator().random_subscription(dynamic=True, num_nodes=10, lamb=2, edge_p=0.2, add_p=0.5, delete_p=0.5, initial_active_nodes=3, max_threshold=2)
		print('graph edges: {}'.format(self.graph.edges.keys()))
		self.edge_adds = [list(edge_adds)]
		print('adds')
		print(edge_adds)
		self.edge_deletes = [list(edge_deletes)]
		print('deletes')
		print(edge_deletes)
		self.canvas = self.create_canvas(self.graph)
		self.interface = self.create_interface(self.graph, self.canvas, self.edge_adds, self.edge_deletes)

def test():
	t = VisualSubscriptionTest()
	t.test()

def random_test():
	r = RandomGraphVisualSubscriptionTest()
	r.test()
if __name__ == '__main__':
	# test()
	random_test()
