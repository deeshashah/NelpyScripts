import nltk

class NgramsFinder(object):
		
	def __init__(self,sentence):

		self.sentence = sentence

		#Inspired from Su Nam Kim Paper...
		self.grammar = r"""
			NBAR:
				{<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
				
			NP:
				{<NBAR>}
				{<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
		"""
		

	def get_bigrams(self):
		"""	Returns a list of all bigrams """		
		chunker = nltk.RegexpParser(self.grammar)
		toks = nltk.word_tokenize(self.sentence)
		postoks = nltk.tag.pos_tag(toks)
		tree = chunker.parse(postoks)
		required_ones = [leave for leave in self.leaves(tree) if len(leave) >= 2]
		return self.get_clean_list(required_ones)
		# return required_ones

	def leaves(self,tree):
		""" Finds NP (nounphrase) leaf nodes of a chunk tree """
		for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
			yield subtree.leaves()

	def get_clean_list(self,required_ones):
		"""
		'required_ones' is not in a usable format, this function does the trick 
		Converting from [[('computer', 'NN'), ('scientist', 'NN')]] to  [['computer', 'scientist']]
		"""
		mainList = []
		for ngram_list in required_ones:
			temp_list = []
			for ngram_tuple in ngram_list:
				temp_list.append(ngram_tuple[0])
			mainList.append(temp_list)
		return mainList