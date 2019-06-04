import random
import pylab
from matplotlib.pyplot import pause
from matplotlib import pyplot as plt
import networkx as nx
import graph
import sys

"""
pylab.ion()
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
pylab.show()

for i in range(num_plots):

    get_fig()
    pylab.draw()
    pause(2)
"""

class DynamicCanvas:
	def __init__(self, drawer=None):
		self.drawer = drawer

	def start(self):
		pylab.ion()
		pylab.show()
		self.drawer.start()
		self.draw_and_wait()

	def step(self, new_graph, adds, deletes):
		self.drawer.step(new_graph, adds, deletes)
		self.draw_and_wait()

	def draw_and_wait(self):
		pylab.draw()
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

	def start(self):
		nx.draw_networkx_nodes(self.nx_graph, self.pos)
		nx.draw_networkx_edges(self.nx_graph, self.pos, edgelist=self.nx_graph.edges(), edge_color='w')
		edgelist = [(e.u.l, e.v.l) for e in self.graph.get_edges()]
		nx.draw_networkx_edges(self.nx_graph, self.pos, edgelist=edgelist, edge_color=self.edge_color)
		self.draw_nodes(self.graph.get_nodes())

	def step(self, new_graph, adds, deletes):
		self.draw_nodes(new_graph.get_nodes())
		self.add_edges(adds)
		self.delete_edges(deletes)
		self.finalize(new_graph, adds, deletes)

	def finalize(self, graph, adds, deletes):
		pass # TODO add subscription times, etc.

	def draw_nodes(self, nodes):
		active, inactive = [], []
		for node in nodes:
			l = active if node.active else inactive
			l.append(node.l)
		nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=active, node_color=self.active_node_color)
		nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=inactive, node_color=self.inactive_node_color)

	def add_edges(self, edges):
		self.draw_edges(edges, self.edge_color)

	def delete_edges(self, edges):
		self.draw_edges(edges, type(self).INVISIBLE)

	def draw_edges(self, edgelist, color):
		nx.draw_networkx_edges(self.nx_graph, self.pos, edgelist, color)

class DynamicSubscriptionDrawer(DynamicDrawer):
	pass

def test1():
	pylab.ion()
	pylab.show()
	g = graph.get_test_graph()
	d = DynamicDrawer(g)
	c = DynamicCanvas(d)
	c.start()
	d.edge_color = 'y'
	g.get_node(1).activate()
	c.start()



if __name__ == '__main__':
	test1()
