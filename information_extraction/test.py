from ie_module.SentenceProcessor import SentenceProcessor
from ie_module.NgramsFinder import NgramsFinder

s = SentenceProcessor('John is a computer scientist',1)
print s.get_parsed_graph()
s.save_dot_graph()

n = NgramsFinder('John lives in the Great Britain')
print n.get_ngrams()