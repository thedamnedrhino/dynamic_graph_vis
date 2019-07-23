import networkx as nx
import matplotlib.pyplot as plt
import graph
import interface

STEPS=5

def create_visual_interface(graph, steps=10, figure_texts=[]):
	return interface.VisualInterfaceFactory().create(graph=graph, n=steps, dynamic=False, display_mode='subplot', figure_texts=figure_texts)

def draw_from_edges(*edges):
	g = nx.Graph()
	g.add_edges_from(edges)
	pos = nx.kamada_kawai_layout(g)
	print(pos)
	nx.draw(g, pos)
	nx.draw_networkx_labels(g, pos)
	plt.show()

def display(graph, steps=10, figure_texts=[]):
	interface = create_visual_interface(graph, steps=steps, figure_texts=figure_texts)
	s = graph.get_node('s')
	interface.start(run=lambda: print(s.active))

def display_subscription_graph(lamb, nodes, active_nodes, edges, steps=10):
	nodeset = {label: graph.SubscriptionNode(label, threshold, lamb) for label, threshold in nodes.items()}
	g = graph.Graph(nodeset, directed=False)
	for l, n in nodeset.items():
		if l in active_nodes:
			n.activate()
	for u, v in edges:
		g.add_edge(u, v)
	display(g, steps, figure_texts=['λ: 2', 'S: {s}'])


class Figs:
	def LAT1(self):
		draw_from_edges(('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('d', 'e'))
	def DTM1(self):
		draw_from_edges(('a', 'c'), ('b', 'c'))
	def SM1(self):
		nodes = {'s': 3, 'i': 1, 'ii': 1, 'Y': 1, 'X': 1, 'a': 2, 'b': 1, 'c': 1, 'I': 2, 'II': 2}
		edges = [('s', 'I'), ('s', 'II'), ('s', 'X'), ('s', 'i'), ('i', 'ii'), ('ii', 'Y'), ('Y', 'a'), ('X', 'a'), ('a', 'b'), ('b', 'c'), ('c', 'a')]
		display_subscription_graph(2, nodes, ['s', 'X'], edges, STEPS)

if __name__== '__main__':
	f = Figs()
	#f.LAT1()
	#f.DTM1()
	f.SM1()

