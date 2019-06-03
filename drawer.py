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

class Drawer:
	def __init__(self):
		self.networkx_edges = None
	def draw(self, graph):
		g = nx.DiGraph()
		g.add_nodes_from([node.l for node in graph.get_nodes()])
		g.add_edges_from([(e.u.l, e.v.l) for e in graph.get_edges()])
		nx.draw(g)
	def update(self, old_graph, new_graph, adds, removes):
		# color the removed edges white
		nx.draw_networkx_edges()

class DynamicDrawer:
	def __init__(self, base_graph):
		self.graph = base_graph
		self.nx_graph = nx.complete_graph([node.l for node in self.graph.get_nodes()])
		self.pos = nx.spring_layout(self.nx_graph)

	def start(self):
		nx.draw_networkx_nodes(self.nx_graph, self.pos)
		nx.draw_networkx_edges(self.nx_graph, self.pos, edgelist=self.nx_graph.edges(), edge_color='w')
		edgelist = [(e.u.l, e.v.l) for e in self.graph.get_edges()]
		nx.draw_networkx_edges(self.nx_graph, self.pos, edgelist=edgelist, edge_color='b')


def test():
	pylab.ion()
	d = Drawer()
	pylab.show()
	g = graph.get_test_graph()
	g.remove_edge(1, 2)
	d.draw(g)
	# plt.show()
	pylab.draw()
	pause(2)
	g = graph.get_test_graph()
	plt.clf()
	d.draw(g)
	# plt.show()
	pylab.draw()
	pause(2)

def test1():
	g = graph.get_test_graph()
	d = DynamicDrawer(g)
	d.start()
	plt.show()



if __name__ == '__main__':
	test1()
