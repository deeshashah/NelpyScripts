from nelpy_module.SentenceProcessor import SentenceProcessor
from nelpy_module.NgramsFinder import NgramsFinder

print "\nDependency parsing of the sentence 'John is a computer scientist' is:"
s = SentenceProcessor('John is a computer scientist',1)
print s.get_parsed_dotgraph()
s.save_dot_graph()

print "\nN-grams in the sentence 'John lives in the Great Britain' are :"
n = NgramsFinder('John lives in the Great Britain')
print n.get_ngrams()

print "\nN-grams when combined in a dotgraph, will look like the following. Consider a sentence 'John is a computer scientist' :"
print s.get_merged_ngrams_dotgraph()
s.save_merged_ngrams_graph()