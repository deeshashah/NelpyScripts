import networkx as nx
import matplotlib.pyplot as plt
from SentenceProcessor import SentenceProcessor
from networkx.drawing.nx_agraph import graphviz_layout
from graphviz import Source
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout
import os

class MultiSentenceGraph(object):

	def __init__(self,sentence_dict):
		self.sentence_dict = sentence_dict

	# Takes a dict of {'index':'sentence'}
	def get_multisentence_merged_graph(self): 
		# Here we will call everythimg that wil create a merged graph


		mg = nx.MultiDiGraph()

		for index,sentence in self.sentence_dict.iteritems():
			mg = self.merge_single_sentence(mg,sentence,index)

		# Printing PageRank score
		print "\n\n PAGERANK \n"
		print nx.pagerank(nx.DiGraph(mg))
		print "\n\n________________________________\n\n"
		
		print mg.nodes(data=True)
		nx.draw(mg,pos=graphviz_layout(mg,prog='neato'),arrows=True,with_labels=True,alpha=0.5,linewidths=0.5,scale=2)
		nx.draw_networkx_edge_labels(mg, pos = graphviz_layout(mg, prog='neato'),labels = nx.get_edge_attributes(mg,'label'))
		# plt.show()
		if(os.path.exists("graph_images/multisentence_graph/combined_multisentence_graph.png")):
			os.remove("graph_images/multisentence_graph/combined_multisentence_graph.png")

		print "Hahahah"
		plt.savefig("graph_images/multisentence_graph/combined_multisentence_graph.png", format = "PNG")

	def merge_single_sentence(self, ng, single_sentence,index):

		print "\n\nNX Code being executed - "
		s = SentenceProcessor(single_sentence,index)

		# single_sentence = "Search engine firm Google has released a trial tool which is concerning some net users because it directs people to pre-selected commercial websites."
		# sentenceTwo = "The AutoLink feature comes with Google's latest toolbar and provides links in a webpage to Amazon.com if it finds a book's ISBN number on the site"

		merged_dotgraph = s.get_merged_ngrams_dotgraph()
		
		# This is where I want to store the bigram merged images
		filepath = "graph_images/ngrams_merged_images/"+str(index)+"merged"
		s = Source(merged_dotgraph, filename=filepath, format="png")
		s.render(filename=filepath)


		# To remove self-loops
		# g.remove_edges_from(g.selfloop_edges())

		# Lets make a multi digraph, so that multiple directed edges are allowed.
		g = nx.drawing.nx_agraph.from_agraph(pygraphviz.AGraph(merged_dotgraph))

		# print g.nodes(data=True)

		# To draw with labels
		# labels=dict((n,d['label']) for n,d in g.nodes(data=True))
		# nx.draw(g,labels=labels,node_size=1000)
		# plt.show()


		# h = nx.DiGraph(nx.drawing.nx_agraph.from_agraph(pygraphviz.AGraph(dotSecond)))

		# h = nx.drawing.nx_agraph.from_agraph(pygraphviz.AGraph(dotSecond))
		# print h.nodes(data=True)

		pg = self.preprocess_graph(g)		
		
		# ph = self.preprocess_graph(h)

		# Now combinign both graphs
		# ng = nx.compose(g,h)
		mg = nx.MultiDiGraph()
		mg.add_nodes_from(pg.nodes(data=True)+ng.nodes(data=True))
		mg.add_edges_from(pg.edges(data=True)+ng.edges(data=True))

		return mg

	# Now preprocessing graphs so that the attributes are converted as node labels
	def preprocess_graph(self,g):
		pg = nx.MultiDiGraph()
		mappingDict = {}
		for i in g.nodes(data=True):
			if 'label'in i[1]:
				label = i[1]['label']
			else:
				label = 'haha'
			labelText = label[label.find("(")+1:label.find(")")]
			mappingDict[i[0]] = labelText
			pg.add_node(labelText)

		for j in g.edges(data=True):
			labelText = j[2]['label']
			pg.add_edge(mappingDict[j[0]],mappingDict[j[1]],label=labelText)
			
		return pg