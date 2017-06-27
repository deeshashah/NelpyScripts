from ie_module.SentenceProcessor import SentenceProcessor

s = SentenceProcessor('John is a computer scientist',1)
print s.get_parsed_graph()
s.save_dot_graph()