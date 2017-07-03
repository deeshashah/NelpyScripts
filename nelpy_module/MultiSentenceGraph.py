import networkx as nx
import matplotlib.pyplot as plt
from mergeBigram import MergeBigram
from networkx.drawing.nx_agraph import graphviz_layout
from graphviz import Source
import networkx as nx
import matplotlib.pyplot as plt
import pydot, pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import pprint, os

class MultiSentenceGraph(object):

	def __init__(self,sentence_dict):
		self.sentence_dict = sentence_dict

	# Takes a dict of {'index':'sentence'}
	def getGraph(self): 
		# Here we will call everythimg that wil create a merged graph

		# pp = pprint.PrettyPrinter(indent=4)
		# sentenceList = sent_tokenize(paragraph)

		mg = nx.MultiDiGraph()

		for index,sent in self.sentence_dict.iteritems():
			mg = self.getMergedGraph(mg,sent,index)

		# Printing PageRank score
		print "\n\n PAGERANK \n"
		print nx.pagerank(nx.DiGraph(mg))
		print "\n\n________________________________\n\n"
		
		print mg.nodes(data=True)
		nx.draw(mg,pos=graphviz_layout(mg,prog='neato'),arrows=True,with_labels=True,alpha=0.5,linewidths=0.5,scale=2)
		nx.draw_networkx_edge_labels(mg, pos = graphviz_layout(mg, prog='neato'),labels = nx.get_edge_attributes(mg,'label'))
		# plt.show()
		if(os.path.exists("static/netXGraph/1.png")):
			os.remove("static/netXGraph/1.png")

		print "Hahahah"
		plt.savefig("static/netXGraph/1.png", format = "PNG")

	def getMergedGraph(self, ng, sentenceOne,index):

		print "\n\nNX Code being executed - "
		m = MergeBigram()

		# sentenceOne = "Search engine firm Google has released a trial tool which is concerning some net users because it directs people to pre-selected commercial websites."
		# sentenceTwo = "The AutoLink feature comes with Google's latest toolbar and provides links in a webpage to Amazon.com if it finds a book's ISBN number on the site"

		dotFirst = m.merge_bigram(sentenceOne)
		# dotSecond = m.merge_bigram(sentenceTwo)
		
		# This is where I want to store the bigram merged images
		filepath = "static/dotGraphImages/"+str(index)+"merged"
		s = Source(dotFirst, filename=filepath, format="png")
		s.render(filename=filepath)


		# To remove self-loops
		# g.remove_edges_from(g.selfloop_edges())

		# Lets make a multi digraph, so that multiple directed edges are allowed.
		g = nx.drawing.nx_agraph.from_agraph(pygraphviz.AGraph(dotFirst))

		# print g.nodes(data=True)

		# To draw with labels
		# labels=dict((n,d['label']) for n,d in g.nodes(data=True))
		# nx.draw(g,labels=labels,node_size=1000)
		# plt.show()


		# h = nx.DiGraph(nx.drawing.nx_agraph.from_agraph(pygraphviz.AGraph(dotSecond)))

		# h = nx.drawing.nx_agraph.from_agraph(pygraphviz.AGraph(dotSecond))
		# print h.nodes(data=True)

		pg = self.preprocessGraph(g)		
		
		# ph = self.preprocessGraph(h)

		# Now combinign both graphs
		# ng = nx.compose(g,h)
		mg = nx.MultiDiGraph()
		mg.add_nodes_from(pg.nodes(data=True)+ng.nodes(data=True))
		mg.add_edges_from(pg.edges(data=True)+ng.edges(data=True))

		return mg

	# Now preprocessing graphs so that the attributes are converted as node labels
	def preprocessGraph(self,g):
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