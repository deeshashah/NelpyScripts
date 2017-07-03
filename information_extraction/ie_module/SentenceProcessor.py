from nltk.parse.stanford import StanfordDependencyParser
from graphviz import Source
from NgramsFinder import NgramsFinder
	
class SentenceProcessor(object):

	def __init__(self,sentence,sentence_id):
		self.sentence = sentence
		self.sentence_id = str(sentence_id)
		self.stanford_parser_dir = "/home/kairos/den/codes/Nelpy/dependencies/stanford-parser/"
	
	
	def get_parsed_graph(self):
		self.initialize_paths()
		dependency_parser = StanfordDependencyParser(path_to_jar=self.my_path_to_jar, path_to_models_jar=self.my_path_to_models_jar)
		parsed_output = dependency_parser.raw_parse(self.sentence)
		return self.get_dot_output(parsed_output)

	def initialize_paths(self):
		self.my_path_to_models_jar = self.stanford_parser_dir + "stanford-parser-3.5.2-models.jar"
		self.my_path_to_jar = self.stanford_parser_dir + "stanford-parser.jar"
		self.filepath = "graph_images/"+self.sentence_id

	def get_dot_output(self,parsed_output):
		dep = parsed_output.next()
		a = list(dep.triples())
		self.dotgraph = dep.to_dot()
		return self.dotgraph	

	def save_dot_graph(self):
		self.get_parsed_graph() # To set the global variable dotgraph
		s = Source(self.dotgraph, filename=self.filepath, format="png")
		s.render(filename=self.filepath, cleanup = False) # 'Cleanup = True', deletes the source file after rendering, also 'view = True' can be used to open the rendered file by default


	def get_merged_ngrams(self):
		dotOriginal = self.get_parsed_graph()
		n = NgramsFinder(self.sentence)
		listBigrams = n.get_ngrams()
		ngrams_combined_dot = self.merge_ngrams(dotOriginal,listBigrams)
		print ngrams_combined_dot

	def merge_ngrams(self,dotOriginal,listBigrams):
		for singleBigram in listBigrams:
			if len(singleBigram) == 2:
					dotOriginal = self.combineInGraph(dotOriginal,singleBigram[0],singleBigram[1])
			else:
				n = len(singleBigram)
				nextTerm = singleBigram[n-1]
				for i in range(1,n):
					dotOriginal = self.combineInGraph(dotOriginal,singleBigram[n-1-i],nextTerm)
					nextTerm = singleBigram[n-1-i]+" "+nextTerm

		dot_modified = dotOriginal
		return dot_modified


	def combineInGraph(self,dotOriginal,bigramZero,bigramOne):
		"""
		Takes a dotgraph and a bigram, and returns a modified dotgraph in which the bigram is combined
		dotOriginal : The dot graph that is to be combined
		bigramZero : A node (a single word)
		bigramOne : A node (a singel word)
		For example : If the bigram is "Computer Scientist" then bigramZero = "Computer" and bigramOne = "Scientist" (or vice versa, doesn't matter)
		The word with lesser references (low level in the dot tree, nearer to leave) gets replaced 
		"""

		splittedList = dotOriginal.splitlines()
		originalBigram = bigramZero+" "+bigramOne

		# Initially Finding line numbers and node numbers of both
		lineIndexFirst = lineIndexSecond = nodeIndexFirst = nodeIndexSecond = -1;
		for index,line in enumerate(splittedList):
			if line.find(bigramZero)!=-1:
				lineIndexFirst = index
				nodeIndexFirst = line.split(" ")[0]
			if line.find(bigramOne)!=-1:
				lineIndexSecond = index
				nodeIndexSecond = line.split(" ")[0]
						
		if nodeIndexFirst == -1 or nodeIndexSecond == -1:
			return dotOriginal

		# Finding count of node references
		countNodeFirst = countNodeSecond = 0;
		for index, line in enumerate(splittedList):
			if line.find(nodeIndexFirst) != -1:
				countNodeFirst = countNodeFirst + 1
			if line.find(nodeIndexSecond) != -1:
				countNodeSecond = countNodeSecond + 1

		# We will replace one with least count
		if countNodeFirst > countNodeSecond:
			replaceTerm = bigramOne
			replaceNodeIndex = nodeIndexSecond
			replaceLine = lineIndexSecond
			withNodeIndex = nodeIndexFirst
			withLine = lineIndexFirst
		else:
			replaceTerm = bigramZero
			replaceNodeIndex = nodeIndexFirst
			replaceLine = lineIndexFirst
			withNodeIndex = nodeIndexSecond
			withLine = lineIndexSecond

		splittedList[replaceLine] = splittedList[replaceLine].replace(replaceTerm,originalBigram)
		splittedList[withLine] = ""

		splittedList.remove("")

		# Replace node index with source
		newSplittedList = []
		for index,line in enumerate(splittedList): 
			if line.find(replaceNodeIndex)!=-1:
				splittedList[index] = line.replace(replaceNodeIndex,withNodeIndex)

		if "" in splittedList:	
			splittedList.remove("")
	
		return "\n".join(splittedList)	