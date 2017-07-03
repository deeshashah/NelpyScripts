from nltk.parse.stanford import StanfordDependencyParser
from graphviz import Source
from NgramsFinder import NgramsFinder
from BigramCombiner import BigramCombiner
	
class SentenceProcessor(object):

	def __init__(self,sentence,sentence_id):
		self.sentence = sentence
		self.sentence_id = str(sentence_id)
		self.stanford_parser_dir = "/home/kairos/den/codes/Nelpy/dependencies/stanford-parser/"
	
	def get_parsed_dotgraph(self):
		self.initialize_paths()
		dependency_parser = StanfordDependencyParser(path_to_jar=self.my_path_to_jar, path_to_models_jar=self.my_path_to_models_jar)
		parsed_output = dependency_parser.raw_parse(self.sentence)
		return self.convert_to_dot(parsed_output)

	def initialize_paths(self):
		self.my_path_to_models_jar = self.stanford_parser_dir + "stanford-parser-3.5.2-models.jar"
		self.my_path_to_jar = self.stanford_parser_dir + "stanford-parser.jar"
		self.filepath = "graph_images/"+self.sentence_id

	def convert_to_dot(self,parsed_output):
		dep = parsed_output.next()
		a = list(dep.triples())
		self.dotgraph = dep.to_dot()
		return self.dotgraph	

	def save_dot_graph(self):
		self.get_parsed_dotgraph() # To set the global variable dotgraph
		s = Source(self.dotgraph, filename=self.filepath, format="png")
		s.render(filename=self.filepath, cleanup = False) # 'Cleanup = True', deletes the source file after rendering, also 'view = True' can be used to open the rendered file by default

	def get_merged_ngrams(self):
		dotOriginal = self.get_parsed_dotgraph()
		n = NgramsFinder(self.sentence)
		listBigrams = n.get_ngrams()
		ngrams_combined_dot = self.merge_ngrams(dotOriginal,listBigrams)
		return ngrams_combined_dot

	def merge_ngrams(self,dotOriginal,listBigrams):
		b = BigramCombiner(dotOriginal)
		for singleBigram in listBigrams:
			if len(singleBigram) == 2:
					dotOriginal = b.merge_bigram(singleBigram[0],singleBigram[1])
			else:
				n = len(singleBigram)
				nextTerm = singleBigram[n-1]
				for i in range(1,n):
					dotOriginal = b.merge_bigram(singleBigram[n-1-i],nextTerm)
					nextTerm = singleBigram[n-1-i]+" "+nextTerm

		return dotOriginal