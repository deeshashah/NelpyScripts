class BigramCombiner(object):

	def __init__(self,dotOriginal):
		self.dotOriginal = dotOriginal
		
	def merge_bigram(self,bigramZero,bigramOne):

		"""
		Takes a dotgraph and a bigram, and returns a modified dotgraph in which the bigram is combined
		dotOriginal : The dot graph that is to be combined
		bigramZero : A node (a single word)
		bigramOne : A node (a singel word)
		For example : If the bigram is "Computer Scientist" then bigramZero = "Computer" and bigramOne = "Scientist" (or vice versa, doesn't matter)
		The word with lesser references (low level in the dot tree, nearer to leave) gets replaced 
		"""

		splittedList = self.dotOriginal.splitlines()
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
			return self.dotOriginal

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