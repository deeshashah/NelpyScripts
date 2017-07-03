from ie_module.SentenceProcessor import SentenceProcessor
from ie_module.NgramsFinder import NgramsFinder

print "\nDependency parsing of the sentence 'John is a computer scientist' is:"
s = SentenceProcessor('John is a computer scientist',1)
print s.get_parsed_dotgraph()
s.save_dot_graph()

print "\nN-grams in the sentence 'John lives in the Great Britain' are :"
n = NgramsFinder('John lives in the Great Britain')
print n.get_ngrams()