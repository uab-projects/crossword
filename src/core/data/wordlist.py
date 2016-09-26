"""
Defines a class for loading and manipulating lists of words that can be used
to solve the crossword
"""
class WordList(object):
	"""
	@attr	_wordlist	list of lists separed by word length containing word
						lists in each index depending on their length
	@attr 	_filename	file name of the loaded word list
	"""
	__slots__ = ["_wordlist","_filename"]

	"""
	Given a file name, containing a word per line, loads the words into a word
	list and stores them in the class in a formatted way

	@param 	filename	file name to load
	"""
	def __init__(self, filename):
		self._filename = filename
		self._format(self._load(filename))

	"""
	Loads a file containing a word per line into a list and returns it

	@param 	filename 	file name to load
	"""
	def _load(self, filename):
		return [line.rstrip('\n').rstrip('\r') for line in open(filename, 'r')]

	"""
	Returns the wordlist in a unique list which each element is a list containing
	all the words with same length that its index

	@param wordlist a list contaning all the words
	@return formatWordList a list where each element is a list contaning
	        the same length words, one list for each word  length
	"""
	def _format(self, wordlist):
		formattedWordDic = {}
		for word in wordlist:
			key = len(word)
			if key not in formattedWordDic.keys():
				formattedWordDic[key] = []
			formattedWordDic[key].append(word)

		formattedWordList = []
		for i in range(max(formattedWordDic.keys())+1):
			if i in formattedWordDic.keys():
				formattedWordList.append(formattedWordDic[i])
			else:
				formattedWordList.append([])
		print("hello")
		self._wordlist = formattedWordList

	"""
	Returns the wordlist as a list of lists where each sublist contains words
	whose length is the index of the list in the main list

	@return 	wordlist
	"""
	def getLists(self):
		return self._wordlist

	"""
	Returns the name of the file where the wordlist came from

	@return 	filename
	"""
	def getOrigin(self):
		return self._filename

	"""
	Returns the wordlist in a human-readable way, by summarizing them into
	counts per word length

	@return 	string containing summary of the counts of the words
	"""
	def __str__(self):
		txt = "WORD COUNT per size:\n"
		wordcount = 0
		for i in xrange(len(self._wordlist)):
			wordlistcount = len(self._wordlist[i])
			txt += " -> Words with %2d letters: %d\n"%(i,wordlistcount)
			wordcount += wordlistcount
		txt += "TOTAL: There are %d words\n"%wordcount
		return txt
