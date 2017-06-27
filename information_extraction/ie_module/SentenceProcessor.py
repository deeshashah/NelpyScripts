from nltk.parse.stanford import StanfordDependencyParser
from graphviz import Source
	
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
		self.my_path_to_models_jar = self.stanford_parser_dir  + "stanford-parser-3.5.2-models.jar"
		self.my_path_to_jar = self.stanford_parser_dir  + "stanford-parser.jar"
		self.filepath = "graph_images/"+self.sentence_id

	def get_dot_output(self,parsed_output):
		dep = parsed_output.next()
		a = list(dep.triples())
		self.dotGraph = dep.to_dot()
		return self.dotGraph	

	def save_dot_graph(self):
		self.get_parsed_graph()
		s = Source(self.dotGraph, filename=self.filepath, format="png")
		s.render(filename=self.filepath, cleanup = False) # 'Cleanup = True', deletes the source file after rendering, also 'view = True' can be used to open the rendered file by default