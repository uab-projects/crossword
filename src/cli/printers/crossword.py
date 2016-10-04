import numpy as np
import sys
import time
import core.data.constants as constants

# Constants
"""
Unknown variable character to show when unassigned variable
"""
DEFAULT_EMPTYCELL = '?'

"""
Pre-defined table character sets
"""
CHAR_TABLESETS = {
	"single":('┌','┬','┐','├','┼','┤','└','┴','┘','│','─'),
	"double":('╔','╦','╗','╠','╬','╣','╚','╩','╝','║','═')
}

"""
Default pre-defined table character set
"""
CHAR_TABLESETS_DEFAULT = CHAR_TABLESETS["single"]

"""
Default spacing
"""
SPACING_DEFAULT = 1

"""
Default frames per second
"""
FRAMES_DEFAULT = 24

"""
A Crossword printer is an object that is able to print in the same location
the crossword given with the assigned variables passed in each print
"""
class CrosswordPrinter(object):
	"""
	@attr	_crossword 	crossword object to print (filled or not)
	@attr 	_period 	number of time to elapse between prints
	@attr 	_lastTime 	timestamp of the last printed update
	@attr 	_charset 	characters to use to generate the board
	@attr 	_emptycell 	character to use when initializing to set unkown values
	@attr 	_spacing 	spacing to use as horizontal margin in cells
	@attr 	_board 		the array containing ASCII values
	@attr 	_isPrinting controls whether the printer is ready to be updated
	"""
	__slots__ = ["_crossword","_period","_lastTime","_charset","_emptycell","_spacing",
	"_board","_isPrinting"]

	"""
	Initializes a new printer given the crossword object

	@param 	crossword 	crossword object to use
	@pram 	frames 		number of frames to print the crossword per second
						set to <=0 to always print
	"""
	def __init__(self, crossword,frames=FRAMES_DEFAULT):
		self._crossword = crossword
		self._period = 1.0/frames if frames > 0 else 0
		self._lastTime = 0
		self._charset = CHAR_TABLESETS_DEFAULT
		self._emptycell = DEFAULT_EMPTYCELL
		self._spacing = SPACING_DEFAULT
		self._isPrinting = False
		self.setupBoard()

	"""
	Initializes a new board with the features of the crossword (rows and cols)
	with empty cells and unknown values
	"""
	def setupBoard(self):
		self._board = np.chararray((self._crossword.getRows(),
			self._crossword.getCols()))
		self._board[:] = constants.CROSSWORD_CELL_EMPTY
		# fill with variables
		for var in self._crossword.getVariables():
			word = np.chararray((var[0],))
			word[:] = self._emptycell
			if var[1] == constants.ORIENT_HOR:
				self._board[var[2][0],][var[2][1]:var[2][1]+var[0]] = word
			else:
				self._board[:,var[2][1]][var[2][0]:var[2][0]+var[0]] = word

	"""
	Starts the printer, printing the initial empty crossword that will be
	filled and storing the cursor position
	"""
	def start(self):
		sys.stdout.write(str(self))
		# save cursor
		sys.stdout.write("\033[s")
		self._isPrinting = True

	"""
	Given a variable and it's supposed value, updates the printed crossword
	with the assigned value, if the framing period allows the function to print
	and the crossword printer is ready (a previous call to start has been made)

	If the value exceeds variable size, value will be printed till it fits in
	the crossword according to the variable and no warning will be thrown

	@param 	variable 	variable to update with an assigned value
	@param 	value 		value to update the variable with
	"""
	def updateVariable(self,variable,value):
		# check if can update
		assert self._isPrinting
		if self._period > (time.time() - self._lastTime):
			return
		else:
			self._lastTime = time.time()
		# board at cursor
		sys.stdout.write("\033[%dA"%(
			self._crossword.getRows()*2-2*variable[2][0]))
		sys.stdout.write("\033[%dC"%(
			2+variable[2][1]*4))
		# write variable
		for i in range(variable[0]):
			sys.stdout.write(value[i])
			if variable[1] == constants.ORIENT_HOR:
				sys.stdout.write("\033[%dC"%(self._spacing*2+1))
			else:
				sys.stdout.write("\033[1D\033[%dB"%(2))
		# restore cursor position
		sys.stdout.write("\033[u")

	"""
	Stops the printer and forces a new call to start to update new variables on
	the crossword
	"""
	def stop(self):
		self._isPrinting = False

	"""
	Updates the crossword given the assigned variable list with the update
	method

	WARNING: The input must be a numpy array

	@param 	solution 	list with solutions to the crossword to print
	"""
	def updateSolution(self,solution):
		period,self._period = self._period,0
		variables = self._crossword.getVariables()
		for i in range(len(solution)):
			self.updateVariable(variables[i],"".join(
				list(map(chr,solution[i]))))
		self._period = period

	"""
	Given the solution of the crossword, prints the crossword with the solution
	applied all at once, applying start & stop methods automatically

	@param 	solution 	list with solutions to the crosswort to print
	"""
	def printSolution(self,solution):
		self.start()
		self.updateSolution(solution)
		self.stop()

	"""
	Returns the current board as a string

	@return beautiful text line-separed containing the board
	"""
	def __str__(self):
		txt = ""
		line_fmt = "{0}"+\
			(self._charset[10]*(self._spacing*2+1)+"{1}")*\
			(self._board.shape[0])+self._charset[10]*\
			(self._spacing*2+1)+"{2}\n"
		init_line = line_fmt.format(self._charset[0],self._charset[1],
			self._charset[2])
		separe_line = line_fmt.format(self._charset[3],self._charset[4],
			self._charset[5])
		end_line = line_fmt.format(self._charset[6],self._charset[7],
			self._charset[8])
		txt += init_line
		for row in range(self._board.shape[0]):
			txt+=self._charset[9]
			for col in range(self._board.shape[1]):
				txt+= " "*self._spacing+self._board[row][col].decode("utf-8")+\
				" "*self._spacing
				if col < self._board.shape[1]-1:
					txt += self._charset[9]
			txt+=self._charset[9]+"\n"
			if row < self._board.shape[0]-1:
				txt+=separe_line
		txt += end_line
		return txt
