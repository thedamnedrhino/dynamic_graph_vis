import random
import collections
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
	def __init__(self, drawer, nrows, ncols, basesize=3, fontsize=8, callbacks={}):
		super(type(self), self).__init__(drawer)
		self.nrows = nrows
		self.ncols = ncols
		self.i = 1
		self.basesize = basesize
		self.fontsize = fontsize
		self.callbacks = callbacks
		self.graph = None

	def start(self, graph, pos=None):
		self.graph = graph
		self.figure()
		self.subplot()
		self.drawer.start(graph, pos)
		self.callback()

	def step(self, new_graph, adds, deletes):
		self.i += 1
		self.graph = new_graph
		self.subplot()
		self.drawer.step(new_graph, adds, deletes)
		self.callback()

	def callback(self):
		if self.i in self.callbacks:
			self.callbacks[self.i](self.drawer, self.graph)

	def finish(self):
		plt.show()

	def figure(self):
		plt.rc('font', size=self.fontsize, weight='bold')
		plt.figure(figsize=(self.nrows*self.basesize, self.ncols*self.basesize))


	def subplot(self):
		plt.subplot(self.nrows, self.ncols, self.i)
		plt.xlim(-1.1, 1.1)
		plt.ylim(-1.3, 1.2)
		plt.text(-1.065, 0.95, str(self.i), bbox={'facecolor': 'powderblue'})

	def draw(self):
		plt.draw()

class DynamicDrawer:
	INVISIBLE = 'w'
	GREY = '0.5'

	COLORS = {'red': 'r'}

	ATTRIBUTE_MAP = {
			'threshold': 't',
			'lambda': 'λ',
			'receiving': 'in',
			'remaining_lambda': 'rλ',
			}

	def __init__(self, dynamic=True, displayed_attributes=['threshold', 'remaining_lambda', 'lambda'],  figure_texts=[]):
		self.dynamic = dynamic
		self.graph = None
		self.old_graph = None
		self.nx_graph = None
		self.is_directed = None
		#self.pos = nx.spring_layout(self.nx_graph)
		# pos = pos if not pos is None else nx.spring_layout
		# self.pos = pos(self.nx_graph)
		self.edge_color = 'b'
		self.uni_color = 'r'
		self.bi_color = self.edge_color
		self.active_node_color = 'g'
		self.inactive_node_color = type(self).GREY
		self.textboxes = []
		self.displayed_attributes = displayed_attributes
		self.figure_texts = figure_texts
		self.ATTRIBUTE_MAP = collections.defaultdict(lambda x: x)
		self.ATTRIBUTE_MAP.update(type(self).ATTRIBUTE_MAP)
		self.displayed_attributes = ['threshold', 'receiving']
		self.colors = type(self).COLORS

	def init_graph(self, graph, pos=None):
		self.graph = graph
		self.is_directed = self.graph.is_directed()
		self.nx_graph = nx.complete_graph([node.l for node in self.graph.get_nodes()])
		if self.is_directed:
			self.nx_graph = self.nx_graph.to_directed()
		self.pos = pos if not pos is None else nx.spring_layout(self.nx_graph)

	def start(self, graph, pos=None):
		self.init_graph(graph, pos)
		self.draw_nodes()
		self.draw_node_attributes()
		self.draw_initial_edges()
		self.draw_figure_texts()

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

	def draw_figure_texts(self):
		# plt.text(1-0.1, 1-0.1, "\n".join(self.figure_texts), bbox={'facecolor': 'wheat',})
		plt.text(-1.065, 1.4, "\n".join(self.figure_texts), bbox={'facecolor': 'wheat',})


	def clear_figure_texts(self):
		for t in self.textboxes:
			t.set_visible(False)

	def draw_nodes(self):
		active, inactive = [], []
		for node in self.nodes():
			l = active if node.active else inactive
			l.append(node.l)
		self._draw_nx_nodes(nodelist=active, node_color=self.active_node_color)
		self._draw_nx_nodes(nodelist=inactive, node_color=self.inactive_node_color)
		self.draw_node_labels()

	def _draw_nx_nodes(self, nodelist, node_color):
		nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=nodelist, node_color=node_color)

	def draw_node_attributes(self):
		for node in self.nodes():
			attrs = node.get_displayed_attributes()
			attrs = {self.ATTRIBUTE_MAP[name]: value for name, value in attrs.items() if self.displayed_attributes == 'all' or name in self.displayed_attributes}
			# attrs: [(attr_name, attr_val)]
			attr_text = "\n".join([":".join(a) for a in attrs.items()])
			x, y = self.pos[node.l]
			# x = x + 0.1 if x < 0.8 else x - 0.3
			# y = y + 0.2 if y < 0.8 else y - 0.2
			x = x - 0.05
			y = y + len(attrs.keys())*0.2
			#box = plt.text(x, y, s=attr_text, bbox=dict(facecolor='wheat', alpha=0.5, fill=False),verticalalignment='center')
			box = plt.text(x, y, s=attr_text, verticalalignment='center')
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
