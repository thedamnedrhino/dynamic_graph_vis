def get_test_graph():
	f = GraphFactory()
	n1 = f.new_node(1, 1)
	n2 = f.new_node(2, 1)
	f.add_edge(1, 2)
	return f.g

def test():
	g = get_test_graph()
	print(g.nodes)
	print(g.edges)
	g.step()
	print(g.nodes)
	n1.activate()
	print(g.nodes)
	g.step()
	print(g.nodes)
	g.remove_edge(1, 2)
	g.step()
	print(g.nodes)

class GraphFactory:
	def __init__(self):
		self.g = Graph()

	def new_node(self, label, threshold):
		node = Node(label, threshold)
		self.g.add_node(node)
		return node

	def add_edge(self, u, v):
		return self.g.add_edge(u, v)


class Graph:
	def __init__(self, nodes={}):
		self.nodes = nodes
		self.edges = {}


	def add_node(self, node):
		self.nodes[node.l] = node

	def add_edge(self, u, v):
		edge = Edge(self.nodes[u], self.nodes[v])
		self.edges[(u, v)] = edge
		return edge

	def remove_edge(self, u=None, v=None, edge=None):
		if edge is None:
			edge = self.edges[(u, v)]
		edge.remove()
		del self.edges[(u, v)]

	def step(self):
		for node in self.nodes.values():
			node.send()
		for node in self.nodes.values():
			node.receive()

	def get_nodes(self):
		return self.nodes.values()

	def get_edges(self):
		return self.edges.values()


class Node:
	def __init__(self, l, threshold, out_edges=[], in_edges=[]):
		self.l = l
		self.threshold = threshold
		self.receiving = 0
		self.out_edges = set(out_edges)
		self.in_edges = set(in_edges)
		self.active = False

	def activate(self):
		self.active = True

	def deactivate(self):
		self.active = False

	def receive(self):
		if self.active:
			return
		self.receiving = len([e for e in self.in_edges if e.active])
		self.active = (self.receiving >= self.threshold)

	def send(self):
		if self.active:
			for e in self.out_edges:
				e.activate()

	def add_in_edge(self, edge):
		self.in_edges.add(edge)

	def add_out_edge(self, edge):
		self.out_edges.add(edge)

	def edge_cut(self, edge):
		if edge in self.out_edges:
			self.out_edges.remove(edge)
		elif edge in self.in_edges:
			self.in_edges.remove(edge)
		else:
			raise Exception('Node "{}" does not have edge "{}"'.format(self, edge))

	def __repr__(self):
		return "(Node, lab: {}, th: {}, act: {})".format(self.l, self.threshold, self.active)

class SubscriptionNode:
	def __init__(self, l, threshold, lamb, out_edges=[], in_edges=[]):
		super(type(self), self).__init__(threshold, out_edges, in_edges)
		self.lamb = lamb
		self.time = 0

	def receive(self):
		self.t += 1
		if self.t >= self.lamb:
			self.active = False
		super(type(self), self).receive()


class Edge:
	def __init__(self, u, v, attach=True):
		"""
		param active: whether this edge is propagating an activation from source to destination
		"""
		self.u = u
		self.v = v
		self.active = False
		if attach:
			self.attach_to_endpoints()

	def attach_to_endpoints(self):
		self.u.add_out_edge(self)
		self.v.add_in_edge(self)

	def remove(self):
		self.u.edge_cut(self)
		self.v.edge_cut(self)

	def activate(self):
		self.active = True

	def deactivate(self):
		self.active = False

	def __repr__(self):
		return "(Edge: {}-{})".format(self.u.l, self.v.l)


if __name__ == '__main__':
	test()
