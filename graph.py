import random

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

	def delete_node(self, node):
		for edge in node.in_edges.union(node.out_edges):
			print(node)
			print(edge)
			self.delete_edge(edge=edge)
		del self.nodes[node.l]

	def add_edge(self, u, v):
		edge = Edge(self.nodes[u], self.nodes[v])
		self.edges[(u, v)] = edge
		return edge

	def delete_edge(self, u=None, v=None, edge=None):
		if edge is None:
			edge = self.edges[(u, v)]
		del self.edges[(edge.u.l, edge.v.l)]
		edge.delete()

	def start(self):
		self._send()
	def step(self):
		self._receive()
		self._send()

	def _send(self):
		for node in self.nodes.values():
			node.send()
	def _receive(self):
		for node in self.nodes.values():
			node.receive()

	def activate_node(self, node):
		self.get_node(node).activate()

	def get_node(self, node):
		if isinstance(node, Node):
			return node
		return self.nodes[node]

	def get_nodes(self):
		return self.nodes.values()

	def get_edges(self):
		return self.edges.values()


class Node:
	def __init__(self, l, threshold, out_edges=[], in_edges=[]):
		self.l = l
		self.threshold = threshold
		self.out_edges = set(out_edges)
		self.in_edges = set(in_edges)
		self.active = False

	def in_degree(self):
		return len(self.in_edges)

	def out_degree(self):
		return len(self.out_edges)

	def set_threshold(self, threshold):
		self.threshold = threshold

	def activate(self):
		self.active = True

	def deactivate(self):
		self.active = False

	def receive(self):
		if self.active:
			return
		self.active = (self.receiving() >= self.threshold)

	def receiving(self):
		return len([e for e in self.in_edges if e.active])

	def send(self):
		for e in self.out_edges:
			e.activate() if self.active else e.deactivate()

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

	def get_displayed_attributes(self):
		return [('threshold', str(self.threshold)), ('receiving', str(self.receiving()))]

	def __repr__(self):
		return "(Node, label: {}, threshold: {}, active: {})".format(self.l, self.threshold, self.active)

class SubscriptionNode(Node):
	def __init__(self, l, threshold, lamb, out_edges=[], in_edges=[]):
		super(type(self), self).__init__(l, threshold, out_edges, in_edges)
		self.lamb = lamb
		self.time = 0

	def send(self):
		super(type(self), self).send()
		self.time += 1

	def receive(self):
		if self.time >= self.lamb:
			self.active = False
		super(type(self), self).receive()
		if not self.active:
			self.time = 0

	def remaining_subscription(self):
		if not self.active:
			return 0
		return self.lamb - self.time

	def get_displayed_attributes(self):
		base = super(type(self), self).get_displayed_attributes()
		return base + [('remaining', str(self.remaining_subscription())), ('lambda', str(self.lamb))]


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

	def delete(self):
		self.u.edge_cut(self)
		self.v.edge_cut(self)

	def activate(self):
		self.active = True

	def deactivate(self):
		self.active = False

	def __repr__(self):
		return "(Edge: {}-{})".format(self.u.l, self.v.l)

class RandomGraphGenerator:
	def random_dynamic_subscription(self, num_nodes, lamb, edge_p, add_p, delete_p, initial_active_nodes=1, max_threshold=1000000):

		nodes = {i: SubscriptionNode(i, None, lamb) for i in range(num_nodes)}
		g = Graph(nodes)
		for n in random.choices(list(nodes.values()), k=initial_active_nodes):
			n.activate()
		edges = self.random_edges(nodes.keys(), edge_p)
		for e in edges:
			g.add_edge(*e)
		degree0s = []
		for n in nodes.values():
			if n.in_degree() is 0:
				degree0s.append(n)
				continue
			n.set_threshold(random.randint(1, min(n.in_degree(), max_threshold) + 1))
		for n in degree0s:
			g.delete_node(n)
		return g, self.random_updates(nodes.keys(), edges, add_p, delete_p)

	def random_edges(self, nodes, p):
		n = len(nodes)
		return ((u, v) for u in nodes for v in nodes if self.bern(p))
	def random_updates(self, nodes, edges, add_p, delete_p):
		adds = [(u, v) for u in nodes for v in nodes if (u, v) not in edges and self.bern(add_p)]
		deletes = (e for e in edges if self.bern(delete_p))
		return adds, deletes
	def bern(self, p):
		return random.random() <= p


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
	g.delete_edge(1, 2)
	g.step()
	print(g.nodes)

if __name__ == '__main__':
	test()
