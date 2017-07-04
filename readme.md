# Nelpy 

This repository contains different modules for performing Natural language processing(NLP) tasks in Python.

Following is the gist of each one of them. Check out individual `README.md`s for more.

### Dependency Parsing

Understanding of Natural Language involves extraction of knowledge. The extraction of information from language can be done in many ways. Deep parsing is one such method which gives intra-sentence dependencies based on the model. Using Stanford parser, sentence level deep parsing is done in `nelpy_module` which can be used as follows. For more information and explanation about the code, refer [this article](put link).

First set up python environment, install dependencies using `requirements.txt`. Follow [this tutorial](put link).

Note : To install `graphviz` and `pygraphviz` in ubuntu, run this command in order. (after activating virtual environment)

```
sudo apt install python-dev graphviz libgraphviz-dev pkg-config
pip install graphviz
pip install pygraphviz
```

Also set your own path of `stanford-parser` in file `SentenceProcessor.py` line number 10.

```python
from nelpy_module.SentenceProcessor import SentenceProcessor

s = SentenceProcessor('John is a computer scientist',1)
print s.get_parsed_dotgraph()
s.save_dot_graph(s)
```

Gives the follwing output.

```dot
digraph G{
edge [dir=forward]
node [shape=plaintext]

0 [label="0 (None)"]
0 -> 5 [label="root"]
1 [label="1 (John)"]
2 [label="2 (is)"]
3 [label="3 (a)"]
4 [label="4 (computer)"]
5 [label="5 (scientist)"]
5 -> 2 [label="cop"]
5 -> 4 [label="compound"]
5 -> 3 [label="det"]
5 -> 1 [label="nsubj"]
}
```

Also saves the graph image in the specified directory.

![Dot Graph]( Put Link )

### Ngrams Finder

In a sentence, it is an important task to  find n-grams that makes sense together (like 'Computer Scientist' or 'Great Britain'). Using POS tag pattern matching, we can solve this problem. Here is how `NgramsFinder` class can be used.

```python
from nelpy_module.NgramsFinder import NgramsFinder

n = NgramsFinder('John lives in the Great Britain')
print n.get_ngrams()
```

The output of the above would be,

```
[['Great', 'Britain']]
```

### Combine N-grams in a sentence

Once we have found out which Ngrams in a sentence are making sense together, we need to represent it a graph. So to make a `dot` formatted graph after combining the Ngrams of a sentence, following code can be used.

```python
from nelpy_module.SentenceProcessor import SentenceProcessor
s = SentenceProcessor('John is a computer scientist',1)
print s.get_merged_ngrams_dotgraph()
s.save_merged_ngrams_graph()
```

The output would be : 

```dot
digraph G{
edge [dir=forward]
node [shape=plaintext]
0 [label="0 (None)"]
0 -> 5 [label="root"]
1 [label="1 (John)"]
2 [label="2 (is)"]
3 [label="3 (a)"]
5 [label="5 (computer scientist)"]
5 -> 2 [label="cop"]
5 -> 5 [label="compound"]
5 -> 3 [label="det"]
5 -> 1 [label="nsubj"]
}
```

And this image would be saved in the specified `filepath`

![put image](here)

Note : The word with lesser references (low level in the dot tree, nearer to leave) gets replaced.  

### Combine many sentences by common nodes

