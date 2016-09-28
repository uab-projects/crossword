# libraries
from .constants import *
from ..helpers.parse import *

#constants
"""
Character to use to fill unassigned variable strings
"""
VARIABLE_FILL = '\0'
"""
Character to use to fill unassigned variable string when showing them to our
loved users
"""
VARIABLE_FILL_SHOW = '?'
"""
Value to use when a map from a real world variable does not exist in the 1D
variables because no variable exists / variable has no length enough
"""
VARIABLE_REAL_UNKOWN = None


"""
Loads, reads and manipulates crossword puzzles in order
to send them to solve later
"""
class Crossword(object):
	"""
	@attr	_crossword		crossword puzze as lists of lists
	@attr	_filename		file the crossword was loaded from
	@attr 	_hasRead 		indicates if the file has read properly
	@attr 	_rows 			number of rows of the crossword
	@attr 	_cols 			number of cols of the crossword
	@attr 	_last_word  	number of max real (hor/ver) variables found
							this is set as the maximum number found in the
							crossword
	@attr 	_hasParsed 		indicates if the contents have parsed properly
	@attr 	_variables 		list of 1D variables to fill as empty strings
							the first variable represents the first horizontal
							variable found and so on
	@attr 	_vars_limit     index of the first variable that is vertical in the
							list of 1D variables
	@attr 	_constraints 	constraints that the crossword contains
							in a list of (a,b,c,d) tuples where those letters
							mean: word a letter b = word c letter d
	@attr 	_from2DVars 	tuple of lists that map the real (2D) vars to the
							indexes of the 1D variables list
								([list of hor_vars],[list of ver vars])
	@attr   _from1DVars     List that given an index from the 1D variable list
							returns a tuple indicating the orientation
							and the number of the real var:
								(orient,real_var_number)
	"""
	__slots__ = ["_crossword","_filename","_hasRead",
	"_rows","_cols","_last_word","_hasParsed","_variables","_vars_limit",
	"_constraints","_from2DVars","_from1DVars"]

	"""
	Initializes a new crossword with empty values

	@param	filename	filename of the crossword to load
	"""
	def __init__(self, filename):
		self._crossword = None
		self._filename = filename
		self._hasRead = False
		self._rows = 0
		self._cols = 0
		self._hasParsed = False
		self._variables = []
		self._vars_limit = 0
		self._constraints = None
		self._from2DVars = (None,None)
		self._from1DVars = []

	"""
	Reads the crossword from the file and transforms it into a list of lists
	saving it to the _crossword attribute

	@throws	IOError 	if error opening file
	@return self, the same instance
	"""
	def read(self):
		self._readFile()
		self._readFeatures()
		self._hasRead = True
		return self

	"""
	Loads the crossword into a list of lists with each item being a line of the
	crossword
	"""
	def _readFile(self):
		crossword = [line.rstrip('\n') for line in open(self._filename, 'r')]
		crossword = list(map(lambda x: x.split("\t"),crossword))
		self._crossword = crossword

	"""
	Finds in the crossword the number of rows and cols and number of variables
	"""
	def _readFeatures(self):
		assert self._crossword != None
		self._rows = len(self._crossword)
		self._cols = len(self._crossword[0])
		self._last_word = max(max(map(
			lambda x: int(x) if isInteger(x) and int(x) > 0 else 0,sl))
			for sl in self._crossword)
		self._from2DVars = (
		[None for _ in range(self._last_word)],
		[None for _ in range(self._last_word)])

	"""
	Parses the values of the crossword to find the variables that have to be
	assigned and the constraints that apply

	A successful call to read() must be done before calling this method

	@throws 	ValueError	if some error found while reading the contents
	@return 	self
	"""
	def parse(self):
		assert self._hasRead
		self._parse()
		return self

	"""
	Reads the crossword finding the variables that must be assigned and the
	constraints that apply, filling the
		_variables
		_contraints
		_from2DVars
		_from1DVars
	attributes with their appropiate values

	A successful call to _readFile() and _readFeatures() must be done before
	calling this method.

	Won't add variable whose size is < constants.WORDS_LEN_MIN

	@throws 	ValueError 	if some character not allowed is found
	"""
	def _parse(self):
		assert self._hasRead
		# init variables
		self._variables = []
		variable = ""
		variable_n = 0
		orient = None
		constraints_table = tuple([
			tuple([[] for __ in range(self._cols)])
				for _ in range(self._rows)])

		# parses the current cell to add constraint / variable
		"""
		Given the i,j coordinates of the crossword of the cell, parses the
		content of the cell and modifies the function current variable read,
		and variable number in order to add variables and constraints

		@param 	i 	crossword row index (0-based)
		@param 	j 	crossword col index (0-based)
		"""
		def __parseCell(i,j):
			nonlocal orient
			nonlocal variable
			nonlocal variable_n
			nonlocal constraints_table
			cell = self._crossword[i][j]
			if len(variable):
				# reading a variable
				if cell == CROSSWORD_CELL_WORD or isInteger(cell):
					constraints_table[i][j].append(
						(len(self._variables),len(variable)))
					variable += VARIABLE_FILL
				elif cell == CROSSWORD_CELL_EMPTY:
					self._addVariable(orient,variable_n,variable)
					variable = ""
			else:
				# not reading variable
				# empty field / other orientation word
				if cell == CROSSWORD_CELL_EMPTY or \
					cell == CROSSWORD_CELL_WORD:
					return
				# numeric field
				elif isInteger(cell):
					variable_n = int(cell)
					constraints_table[i][j].append(
						(len(self._variables),len(variable)))
					variable += VARIABLE_FILL
				# field unknown
				else:
					raise ValueError("unknown cell value %s "%(cell)
					+"while parsing crossword cell [%d][%d]"%(i+1,j+1))

		# read horizontal
		orient = ORIENT_HOR
		for i in range(self._rows):
			for j in range(self._cols):
				__parseCell(i,j)
			# end of row
			self._addVariable(orient,variable_n,variable)
			variable = ""

		# set horizontal limit
		self._vars_limit = len(self._variables)

		# read vertical
		orient = ORIENT_VER
		for j in range(self._cols):
			for i in range(self._rows):
				__parseCell(i,j)
			# end of col
			self._addVariable(orient,variable_n,variable)
			variable = ""

		# set constraints to list
		self._constraints = tuple([[] for _ in range(len(self._variables))])
		for i in range(self._rows):
			for j in range(self._cols):
				constraints = constraints_table[i][j]
				if len(constraints) == 2:
					self._constraints[constraints[0][0]].append(
						(constraints[0][1],constraints[1][0],
						constraints[1][1]))
					self._constraints[constraints[1][0]].append(
						(constraints[1][1],constraints[0][0],
						constraints[0][1]))
				elif len(constraints) > 2:
					raise ValueError("More than 2 constraints on a 2D world, "
					+"I think you're wrong ;) (or maybe I'm)")
		self._hasParsed = True

	"""
	Sets the plain 1D variable index equivalent of the given combination of
	orientation, variable number that represent a 2D variable

	@param 	orient 	orientation of the real variable
	@param 	num 	number of the real variable
	@param 	index 	index in the list of plain variables
	"""
	def _set1DVarFrom2DVar(self, orient, num, index):
		self._from2DVars[orient][num-1] = index

	"""
	Sets the 2D variable orientation / variable_num equivalent given the
	index of the 1D variable list

	@param 	orient 	orientation of the real variable
	@param 	num 	number of the real variable
	@param 	index 	index in the list of plain variables
	"""
	def _set2DVarFrom1DVar(self, orient, num, index):
		# enlarge list if necessary
		while index >= len(self._from1DVars):
			self._from1DVars.append(VARIABLE_REAL_UNKOWN)
		# write into it
		self._from1DVars[index] = (orient,num)

	"""
	Sets the equivalence of a 2D variable to a 1D variable from both sides
	(1D variable to 2D variable and vice versa)

	@param 	orient 	orientation of the real variable
	@param 	num 	number of the real variable (in the crossword)
	@param 	index 	index in the list of plain (1D) variables
	"""
	def _setVariableRelation(self, orient, num, index):
		self._set1DVarFrom2DVar(orient,num,index)
		self._set2DVarFrom1DVar(orient,num,index)

	"""
	Adds a new variable to assign, and saves the relation between the 1D plain
	list and the 2D real variables

	Also checks if the variable has at least minimum size in order to add it or
	not

	@param 	orient 		orientation of the real variable
	@param 	num 		number of the real variable (in the crossword)
	@param 	variable 	variable to add
	"""
	def _addVariable(self, orient, num, variable):
		if(len(variable) >= WORDS_LEN_MIN):
			index = len(self._variables)
			self._variables.append(variable)
			self._setVariableRelation(orient,num,index)

	"""
	Returns the name of the file loaded

	@return		filename
	"""
	def getOrigin(self):
		return self._filename


	"""
	Returns the crossword as a list of rows

	Previously a successful call to read() must be done

	@return		crossword as list of rows
	"""
	def getLists(self):
		assert self._hasRead
		return self._crossword

	"""
	Returns the number of rows in the crossword

	WARNING: Must be called after reading file

	@return 	rows in the crossword
	"""
	def getRows(self):
		assert self._hasRead
		return self._rows

	"""
	Returns the number of cols in the crossword

	WARNING: Must be called after reading file

	@return 	cols in the crossword
	"""
	def getCols(self):
		assert self._hasRead
		return self._cols

	"""
	Returns the maximum number of real variables in the crossword (the highest
	number written on the crossword

	WARNING: Must be called after reading file

	@return 	maximum number of a real variable, either hor / ver
	"""
	def getLastWordNumber(self):
		assert self._hasRead
		return self._last_word

	"""
	Returns the constraints as a list of tuples (a,b,c,d) that means that
	variable a, letter b must be equal to variable c letter d

	Previously a successful call to parse() must be done

	@return 	constraints
	"""
	def getConstraints(self):
		assert self._hasParsed
		return self._constraints

	"""
	Returns the crossword as a list of unassigned variables

	Previously a successful call to parse() must be done

	@return		unassigned variables of the crossword
	"""
	def getVariables(self):
		assert self._hasParsed
		return self._variables

	"""
	Given the index of a variable in the 1D variable list, returns a tuple
	indicating the real variable that represents that variable

	@param 	index 	index of the 1D variable to get real variable equivalent
	@return tuple: (orient, number) representing real orientation and number
	"""
	def get2DVariable(self, index):
		return self._from1DVars[index]

	"""
	Given the orientation and number of a variable, returns the index of it's
	equivalent variable in the 1D list or VARIABLE_REAL_UNKOWN (None) if no
	mapping exists. See VARIABLE_REAL_UNKOWN definition to see cases where it
	does not exist a mapping

	@param 	orient 	orientation of the variable
	@param 	num 	number of the variable (1-based)
	@return index of the 1D variable or VARIABLE_REAL_UNKOWN if not exists map
	"""
	def get1DVariable(self, orient, num):
		return self._from2DVars[orient][num-1]

	"""
	Reads the crossword finding the variables that must be filled and fills in a
	new crossword all the variables. Uses the following attributes
		_crossword
		_variables
		_from2DVars
		_from1DVars
	attributes with their appropiate values

	A successful call to read() and parse() must be done before calling this
	method

	@param 		variables filled to fill in the crossword
	@throws 	ValueError 	if some character not allowed is found
	"""
	def applyVariables(self, variables):
		assert self._hasParsed
		assert len(self._variables) == len(variables)
		# init variables
		variable = ""
		variable_n = 0
		orient = None
		filled_crossword = [[CROSSWORD_CELL_EMPTY for __ in range(self._cols)]\
		 for _ in range(self._rows)]

		# parses the current cell to add constraint / variable
		"""
		Given the i,j coordinates of the crossword of the cell, parses the
		content of the cell and modifies the function current variable read,
		and variable number in order to add variables and constraints

		@param 	i 	crossword row index (0-based)
		@param 	j 	crossword col index (0-based)
		"""
		def __parseCell(i,j):
			nonlocal orient
			nonlocal variable
			nonlocal variable_n
			nonlocal constraints_table
			cell = self._crossword[i][j]
			if len(variable):
				# reading a variable
				if cell == CROSSWORD_CELL_WORD or isInteger(cell):
					constraints_table[i][j].append(
						(len(self._variables),len(variable)))
					variable += VARIABLE_FILL
				elif cell == CROSSWORD_CELL_EMPTY:
					self._addVariable(orient,variable_n,variable)
					variable = ""
			else:
				# not reading variable
				# empty field / other orientation word
				if cell == CROSSWORD_CELL_EMPTY or \
					cell == CROSSWORD_CELL_WORD:
					return
				# numeric field
				elif isInteger(cell):
					variable_n = int(cell)
					constraints_table[i][j].append(
						(len(self._variables),len(variable)))
					variable += VARIABLE_FILL
				# field unknown
				else:
					raise ValueError("unknown cell value %s "%(cell)
					+"while parsing crossword cell [%d][%d]"%(i+1,j+1))

		# read horizontal
		orient = ORIENT_HOR
		for i in range(self._rows):
			for j in range(self._cols):
				__parseCell(i,j)
			# end of row
			self._addVariable(orient,variable_n,variable)
			variable = ""

		# set horizontal limit
		self._vars_limit = len(self._variables)

		# read vertical
		orient = ORIENT_VER
		for j in range(self._cols):
			for i in range(self._rows):
				__parseCell(i,j)
			# end of col
			self._addVariable(orient,variable_n,variable)
			variable = ""

		# set constraints to list
		self._constraints = tuple([[] for _ in range(len(self._variables))])
		for i in range(self._rows):
			for j in range(self._cols):
				constraints = constraints_table[i][j]
				if len(constraints) == 2:
					self._constraints[constraints[0][0]].append(
						(constraints[0][1],constraints[1][0],
						constraints[1][1]))
					self._constraints[constraints[1][0]].append(
						(constraints[1][1],constraints[0][0],
						constraints[0][1]))
				elif len(constraints) > 2:
					raise ValueError("More than 2 constraints on a 2D world, "
					+"I think you're wrong ;) (or maybe I'm)")
		self._hasParsed = True

	"""
	Returns the crossword attributes in a human-readable format

	@return		string containing visual representation of the crossword
	"""
	def __str__(self):
		txt =  "CROSSWORD specifications:\n"
		txt += "------------------------------------------------------------\n"
		txt += "ORIGIN:  %s\n"%(self._filename)
		txt += "STATUS:  %s, %s\n"%(
			"read" if self._hasRead else "not read",
			"parsed" if self._hasParsed else "not parsed")
		if self._hasRead:
			txt += "SIZE:    %d rows x %d cols\n"%(self._rows,self._cols)
			txt += "VARS:    Maximum real variable number is %d\n"\
				%self._last_word
		if self._hasParsed:
			txt += "NAVL:    %s (total: %d)\n"%(
			str(list(map(
				lambda s: s.replace(VARIABLE_FILL,VARIABLE_FILL_SHOW),
				self._variables))),len(self._variables))
			def realVar(i):
				var=self.get2DVariable(i)
				txt="H%02d" if var[0] == ORIENT_HOR else "V%02d"
				return txt%var[1]
			txt += "MAP:     %s (total: %d)\n"%(list(map(
				realVar,range(len(self._variables)))),len(self._variables))
			txt += "LIMIT:   First vertical variable is variable %d (0-index)"\
			%(self._vars_limit)+"\n"
			txt += "CNSTR:   %s (total: %d)\n"%(self._constraints,
				len(self._constraints))
		return txt
