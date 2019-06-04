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
    pause(2)
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

	def draw_and_wait(self):
		plt.draw()
		plt.waitforbuttonpress()

class DynamicDrawer:
	INVISIBLE = 'w'
	GREY = '0.5'

	def __init__(self, base_graph):
		self.graph = base_graph
		self.nx_graph = nx.complete_graph([node.l for node in self.graph.get_nodes()])
		# self.pos = nx.spring_layout(self.nx_graph)
		self.pos = nx.circular_layout(self.nx_graph)
		self.edge_color = 'b'
		self.active_node_color = 'g'
		self.inactive_node_color = type(self).GREY
		self.textboxes = []

	def start(self):
		self.draw_nodes(self.graph.get_nodes())
		self.draw_node_attributes(self.graph.get_nodes())
		nx.draw_networkx_labels(self.nx_graph, self.pos)
		nx.draw_networkx_edges(self.nx_graph, self.pos, edgelist=self.nx_graph.edges(), edge_color='w')
		edgelist = [(e.u.l, e.v.l) for e in self.graph.get_edges()]
		nx.draw_networkx_edges(self.nx_graph, self.pos, edgelist=edgelist, edge_color=self.edge_color)

	def step(self, new_graph, adds, deletes):
		self.draw_nodes(new_graph.get_nodes())
		self.add_edges(adds)
		self.delete_edges(deletes)
		self.finalize(new_graph, adds, deletes)

	def finalize(self, graph, adds, deletes):
		self.clear_figure_texts()
		self.draw_node_attributes(graph.get_nodes())

	def clear_figure_texts(self):
		for t in self.textboxes:
			t.set_visible(False)

	def draw_nodes(self, nodes):
		active, inactive = [], []
		for node in nodes:
			l = active if node.active else inactive
			l.append(node.l)
		nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=active, node_color=self.active_node_color)
		nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=inactive, node_color=self.inactive_node_color)

	def draw_node_attributes(self, nodes):
		for node in nodes:
			attrs = node.get_displayed_attributes()
			# attrs: [(attr_name, attr_val)]
			attr_text = "\n".join([": ".join(a) for a in attrs])
			x, y = self.pos[node.l]
			box = plt.text(x+0.1, y+0.1, s=attr_text, bbox=dict(facecolor='wheat', alpha=0.5),verticalalignment='center')
			self.textboxes.append(box)

	def add_edges(self, edges):
		self.draw_edges(edges, self.edge_color)

	def delete_edges(self, edges):
		self.draw_edges(edges, type(self).INVISIBLE)

	def draw_edges(self, edgelist, color):
		nx.draw_networkx_edges(self.nx_graph, self.pos, edgelist, color)

class DynamicSubscriptionDrawer(DynamicDrawer):
	pass

def test1():
	plt.ion()
	#plt.show()
	g = graph.get_test_graph()
	d = DynamicDrawer(g)
	c = DynamicCanvas(d)
	c.start()
	d.edge_color = 'y'
	g.get_node(1).activate()
	c.start()



if __name__ == '__main__':
	test1()
