import random
from matplotlib.pyplot import pause
from matplotlib import pyplot as plt
import networkx as nx
import graph
import sys

"""
plt.ion()
graph = nx.Graph()
node_number = 0
graph.add_node(node_number, Position=(random.randrange(0, 100), random.randrange(0, 100)))

def get_fig():
    global node_number
    node_number += 1
    graph.add_node(node_number, Position=(random.randrange(0, 100), random.randrange(0, 100)))
    graph.add_edge(node_number, random.choice(graph.nodes()))
    nx.draw(graph, pos=nx.get_node_attributes(graph,'Position'))

num_plots = 50;
plt.show()
for i in range(num_plots):

    get_fig()
    plt.draw()
"""
class DynamicCanvas:
	def __init__(self, drawer=None):
		self.drawer = drawer

	def start(self):
		plt.ion()
		plt.show()
		self.drawer.start()
		self.draw_and_wait()

	def step(self, new_graph, adds, deletes):
		self.drawer.step(new_graph, adds, deletes)
		self.draw_and_wait()

	def finish(self):
		pass

	def draw_and_wait(self):
		plt.draw()
		plt.waitforbuttonpress()

class SubplotCanvas(DynamicCanvas):
	def __init__(self, drawer, nrows, ncols):
		super(type(self), self).__init__(drawer)
		self.nrows = nrows
		self.ncols = ncols
		self.i = 1

	def start(self):
		self.figure()
		self.subplot()
		self.drawer.start()

	def step(self, new_graph, adds, deletes):
		self.subplot()
		self.drawer.step(new_graph, adds, deletes)

	def finish(self):
		plt.show()

	def figure(self):
		base = 5
		plt.figure(figsize=(self.nrows*base, self.ncols*base))

	def subplot(self):
		plt.subplot(self.nrows, self.ncols, self.i)
		self.i += 1

	def draw(self):
		plt.draw()

class DynamicDrawer:
	INVISIBLE = 'w'
	GREY = '0.5'

	def __init__(self, base_graph, dynamic=True, pos=None):
		self.graph = base_graph
		self.dynamic = dynamic
		self.old_graph = None
		self.is_directed = self.graph.is_directed()
		self.nx_graph = nx.complete_graph([node.l for node in self.graph.get_nodes()])
		if self.is_directed:
			self.nx_graph = self.nx_graph.to_directed()
		# self.pos = nx.spring_layout(self.nx_graph)
		pos = pos if not pos is None else nx.spring_layout
		self.pos = pos(self.nx_graph)
		self.edge_color = 'b'
		self.uni_color = 'r'
		self.bi_color = self.edge_color
		self.active_node_color = 'g'
		self.inactive_node_color = type(self).GREY
		self.textboxes = []

	def start(self):
		self.draw_nodes()
		self.draw_node_attributes()
		self.draw_initial_edges()

	def draw_initial_edges(self):
		self.draw_base()
		self.draw_edges()

	def step(self, new_graph=None, adds=[], deletes=[]):
		self.old_graph = self.graph
		self.graph = new_graph if self.dynamic else self.graph
		self.draw_nodes()
		# self.draw_node_attributes()
		self.draw_edges()
		self.finalize(new_graph, adds, deletes)
		"""
		self.add_edges(adds)
		self.delete_edges(deletes)
		"""

	def finalize(self, graph, adds, deletes):
		if self.dynamic:
			self.clear_figure_texts()
		self.draw_node_attributes()

	def clear_figure_texts(self):
		for t in self.textboxes:
			t.set_visible(False)

	def draw_nodes(self):
		active, inactive = [], []
		for node in self.nodes():
			l = active if node.active else inactive
			l.append(node.l)
		nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=active, node_color=self.active_node_color)
		nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=inactive, node_color=self.inactive_node_color)
		self.draw_node_labels()


	def draw_node_attributes(self):
		for node in self.nodes():
			attrs = node.get_displayed_attributes()
			# attrs: [(attr_name, attr_val)]
			attr_text = "\n".join([": ".join(a) for a in attrs])
			x, y = self.pos[node.l]
			box = plt.text(x+0.1, y+0.1, s=attr_text, bbox=dict(facecolor='wheat', alpha=0.5),verticalalignment='center')
			self.textboxes.append(box)

	def draw_node_labels(self):
		nx.draw_networkx_labels(self.nx_graph, self.pos)

	def add_edges(self, edges):
		self.draw_edges(edges, self.edge_color)

	def delete_edges(self, edges):
		self.draw_edges(edges, type(self).INVISIBLE)

	def draw_edges(self):
		edges = self.edge_set()
		if not self.is_directed:
			self.draw_edges_raw(edges, self.edge_color)
			return
		complete_edges = set(self.nx_graph.edges())
		bi_edges = [(u, v) for (u, v) in edges if (v, u) in edges]
		uni_edges = edges.difference(bi_edges)
		self.draw_base()
		if self.old_graph is None:
			self.draw_edges_raw(uni_edges, self.uni_color)
			self.draw_edges_raw(bi_edges, self.bi_color)


	def edge_set(self):
		return set([(e.u.l, e.v.l) for e in self.graph.get_edges()])
	def nodes(self):
		return self.graph.get_nodes()

	def draw_base(self):
		"""
		draws (overwrites) the underlying complete graph with invisible link
		"""
		nx.draw_networkx_edges(self.nx_graph, self.pos, edgelist=self.nx_graph.edges(), edge_color=type(self).INVISIBLE)

	def draw_edges_raw(self, edgelist, color):
		nx.draw_networkx_edges(self.nx_graph, self.pos, edgelist=edgelist, edge_color=color)

class DynamicSubscriptionDrawer(DynamicDrawer):
	pass

def test1():
	plt.ion()
	g = graph.get_test_graph()
	d = DynamicDrawer(g)
	c = DynamicCanvas(d)
	c.start()
	d.edge_color = 'y'
	g.get_node(1).activate()
	c.start()



if __name__ == '__main__':
	test1()
