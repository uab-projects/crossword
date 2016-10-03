import numpy as np

# constants
"""
Number of words to save as head
"""
WORDS_HEAD = 5

"""
Number of words to save as tail
"""
WORDS_TAIL = WORDS_HEAD

"""
Defines a class for loading and manipulating lists of words that can be used
to solve the crossword
"""
class WordList(object):
	"""
	@attr	_wordlist	first, list of words loaded from the specified file
						after parse, list of lists separed by word length
						containing word lists in each index depending on their
						length
	@attr 	_wordcount 	number of words in the dictionary
	@attr 	_filename	file name of the loaded word list
	@attr 	_hasRead 	True if has read the file properly
	@attr 	_hasParsed 	True if has parsed the words properly
	@attr 	_head 		First words found
	@attr 	_tail 		Last words found
	"""
	__slots__ = ["_wordlist","_filename","_wordcount","_hasRead","_hasParsed",
	"_head","_tail"]

	"""
	Initializes an empty wordlist, with a filename to load when calling the read
	method

	@param 	filename	file name to load
	"""
	def __init__(self, filename):
		self._filename = filename
		self._hasRead = False
		self._wordcount = 0
		self._hasParsed = False

	"""
	Reads from the filename saved the word list and stores into a list of
	words

	@raises 	IOError 	if unable to read from file
	@return 	self
	"""
	def read(self):
		self._read()
		self._hasRead = True
		return self

	"""
	Reads a file containing a word per line into a list
	"""
	def _read(self):
		self._wordlist = np.genfromtxt(self._filename,
		dtype=np.str,
		converters={0:lambda x: x})
		self._wordcount = len(self._wordlist)
		self._head = self._wordlist[:WORDS_HEAD]
		self._tail = self._wordlist[-WORDS_TAIL:]

	"""
	Parses the wordlist to transform them into a list of sublists, where each
	sublist contains the number of words whose length is the index of that list
	in the first list

	@return 	self
	"""
	def parse(self):
		assert self._hasRead
		self._parse()
		self._hasParsed = True
		return self

	"""
	Sets the wordlist in a unique list which each element is a list containing
	all the words with same length that its index
	"""
	def _parse(self):
		self._wordlist = [np.array([np.array(list(w))
			for w in self._wordlist if len(w) == num])
			for num in set(len(i) for i in self._wordlist)]
		# check empty sizes
		i=0
		while i < len(self._wordlist):
			if len(self._wordlist[i]) == 0 or len(self._wordlist[i][0]) == i:
				i+=1
			elif len(self._wordlist[i][0]) > i:
				self._wordlist.insert(i,[])

	"""
	Returns the name of the file where the wordlist came from

	@return 	filename
	"""
	def getOrigin(self):
		return self._filename

	"""
	Returns the number of words in the current wordlist / 0 if not loaded yet

	@return 	number of words in the wordlist
	"""
	def __len__(self):
		return self._wordcount

	"""
	Returns the wordlist as a list of lists where each sublist contains words
	whose length is the index of the list in the main list or just a simple
	list of words, depending on the status of the object

	WARNING: At least a successful call to read() is necessary

	@return 	wordlist
	"""
	def getList(self):
		assert self._hasRead
		return self._wordlist

	"""
	Returns the wordlist in a human-readable way, by summarizing them into
	counts per word length

	@return 	string containing summary of the counts of the words
	"""
	def __str__(self):
		txt =  "WORDLIST specifications:\n"
		txt += "------------------------------------------------------------\n"
		txt += "ORIGIN:  %s\n"%(self._filename)
		txt += "STATUS:  %s, %s\n"%(
			"read" if self._hasRead else "not read",
			"parsed" if self._hasParsed else "not parsed")
		if self._hasRead:
			txt += "SIZE:    %d words\n"%(self._wordcount)
			txt += "HEAD:    %s\n"%(self._head)
			txt += "TAIL:    %s\n"%(self._tail)
		if self._hasParsed:
			txt += "MAX_LEN: %d\n"%(len(self._wordlist)-1)
			txt += "COUNTs:  "
			for i in range(len(self._wordlist)):
				txt += "%d->%d"%\
					(i,len(self._wordlist[i]))
				if i != len(self._wordlist)-1:
					txt += ", "
		return txt
