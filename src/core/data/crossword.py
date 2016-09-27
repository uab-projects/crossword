from .constants import *
from ..helpers.parse import *

"""
Loads, reads and manipulates crossword puzzles in order
to send them to solve later
"""
class Crossword(object):
	"""
	@attr	_crossword	crossword puzze as lists of lists
	"""
	__slots__ = ["_crossword","_filename","_constraints"]

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
		navl = []
		navl_i = 0
		var = ""
		rows = len(self._crossword)
		cols = len(self._crossword[0])

		# read horizontal
		for i in range(rows):
			for j in range(cols):
				item = self._crossword[i][j]
				if len(var):
					# reading a variable
					if item == CROSSWORD_CELL_WORD or isInteger(item):
						var += " "
					elif item == CROSSWORD_CELL_EMPTY:
						if len(var) > 1:
							words_horizontal[var_n]=navl_i
							navl.append(var)
							navl_i+=1
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
				words_horizontal[var_n]=navl_i
				navl.append(var)
				navl_i+=1
			var = ""

		#reinitialization of variables
		var = ""

		# read vertical
		for j in range(cols):
			for i in range(rows):
				item = self._crossword[i][j]
				if len(var):
					# reading a variable
					if item == CROSSWORD_CELL_WORD or isInteger(item):
						var += " "
					elif item == CROSSWORD_CELL_EMPTY:
						if len(var) > 1:
							words_vertical[var_n]=navl_i
							navl.append(var)
							navl_i+=1
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
				words_vertical[var_n]=navl_i
				navl.append(var)
				navl_i+=1
			var = ""


		#convers tuple
		words_horizontal_count = max(words_horizontal.keys())
		words_vertical_count = max(words_vertical.keys())
		vars_count = max(words_vertical_count, words_horizontal_count)

		# create empty variables list
		"""navl = (["" for _ in range(vars_count)],
		["" for _ in range(vars_count)])
		for i in range(vars_count):
			try:
				navl[ORIENT_HOR][i] = words_horizontal[i+1]
			except KeyError:
				pass
			try:
				navl[ORIENT_VER][i] = words_vertical[i+1]
			except KeyError:pass#"""

		#PARa JOEL leido en castellano: Jo,el
		#print(len(navl[0]),len(navl[1]))
		#print(len(navl[1][9]))
		return navl

	"""
	Returns the name of the file loaded

	@return		filename
	"""
	def getOrigin(self):
		return self._filename

	"""
	Returns the constraints

	Previously a call to getNAVL must be done in order to have some value

	@return 	constraints
	"""
	def getConstraints(self):
		return self._constraints

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
"""
dic ={}

dic[(3,5)]=(0,[variables])

if .... :
	dic[(3,5)][0] ++
	dic[(3,5)[1].append()

dic[(3,5)]=[(2,
(3,1)]
"""
