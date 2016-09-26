from constants import *
from ..helpers.parse import *

"""
Loads, reads and manipulates crossword puzzles in order
to send them to solve later
"""
class Crossword(object):
	"""
	@attr	_crossword	crossword puzze as lists of lists
	"""
	__slots__ = ["_crossword","_filename"]

	"""
	Initializes a new crossword reading the contents of a file

	@param	filename	filename of the crossword to load
	"""
	def __init__(self, filename):
		self._load(filename)

	"""
	Loads the crossword into a list of lists with each item being a line of the
	crossword

	@param	filename	file to load
	@return crossword loaded as list of lists
	"""
	def _load(self,filename):
		crossword = [line.rstrip('\n') for line in open(filename, 'r')]
		crossword = list(map(lambda x: x.split("\t"),crossword))
		self._crossword = crossword

	"""
	Formats a list of lists representing a crossword into an array of variables
	that have to be filled

	@return		a list of unassigned variables represented as a tuple for h &
	v variables
	"""
	def _format(self):
		#(horizontal,vertical)
		words_horizontal = {}
		words_vertical = {}
		# read horizontal
		var = ""
		var_n = 0
		for line in self._crossword:
			for item in line:
				if len(var):
					# reading a variable
					if item == CROSSWORD_CELL_WORD or isInteger(item):
						var += " "
					elif item == CROSSWORD_CELL_EMPTY:
						if len(var) > 1:
							words_horizontal[var_n]=var
						var = ""
				else:
					# not reading variable
					# empty field / other orientation word
					if item == CROSSWORD_CELL_EMPTY or \
						item == CROSSWORD_CELL_WORD:
						continue
					# numeric field
					elif isInteger(item):
						var_n = int(item)
						var += " "
			# end of line
			if len(var) > 1:
				words_horizontal[var_n]=var
			var = ""
		print(navl)
		return navl

	"""
	Returns the name of the file loaded

	@return		filename
	"""
	def getOrigin(self):
		return self._filename

	"""
	Returns the crossword as a list of rows

	@return		crossword as list of rows
	"""
	def getLists(self):
		return self._crossword

	"""
	Returns the crossword as a list of unassigned variables

	@return		unassigned variables of the crossword
	"""
	def getNAVL(self):
		return self._format()
