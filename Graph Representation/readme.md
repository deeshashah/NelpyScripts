# Graph Representation

Sometimes when working with long paragraphs in NLP, knowledge representations become a task. Graphs are an efficient way of representating information contained in paragraphs. However, if the paragraphs are too long, the graph becomes cluttered and difficult to clearly visualise.

Thus, in this module, we have used javascript(D3.js) to create an interactive graph. 

D3.js is a javascript library that provides an efficient way of adding interactions to the data representations in web browsers. It makes use of SVG, HTML5 and CSS standards. It provides visual control.

To learn D3.js, [D3.js](https://d3js.org/)
In this repository, we have created a visual graph for the following paragraph : 
```
A Christmas tree that can receive text messages has been unveiled at London's Tate Britain art gallery.
The spruce has an antenna which can receive Bluetooth texts sent by visitors to the Tate. The messages will be "unwrapped" by sculptor Richard Wentworth, who is responsible for decorating the tree with broken plates and light bulbs.
```

The d3.js code is in the _graph.html_ file. 

The paragraph needs to be converted into a Json format, which is used by D3.js to create the visual graph.

We have used python's networkX package to convert the paragraph to a json. The Json data is stored in the file _myGraphdata.json_

In order to convert data to a Json format, following the code:
```python
d = json_graph.node_link_data(mg,attrs={'source': 'source', 'target': 'target', 'key': 'key', 'id': 'id'}) #Json format
		json.dump(d, open('static/js/data/myGraphdata.json','w'))
```

More about networkX, [networkX](http://networkx.readthedocs.io/en/networkx-1.10/)

#### Output 

<kbd>![normal](https://raw.githubusercontent.com/rikenshah/Nelpy/Graph%Representation/master/workingScreenshot.png)</kbd>
