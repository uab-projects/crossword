import numpy as np
from core.data.constants import *
import sys
import time

"""
Unknown variable character to show when unassigned variable
"""
CHAR_UNKNOWN = '?'

"""
Character set to use
"""
CHAR_TABLESET_SINGLE = ('┌','┬','┐','├','┼','┤','└','┴','┘','│','─')

"""
A Crossword printer is an object that is able to print in the same location
the crossword given with the assigned variables passed in each print
"""
class CrosswordPrinter(object):
	"""
	@attr	_crossword 	crossword object to print
	"""
	__slots__ = ["_crossword","_charset","_spacing","_board"]

	"""
	Initializes a new printer given the crossword object

	@param 	crossword 	crossword object to use
	@param 	charset 	charset to use to generate beatiful tables
	"""
	def __init__(self, crossword,charset=CHAR_TABLESET_SINGLE,spacing=1):
		self._crossword = crossword
		self._charset = charset
		self._spacing = spacing
		self._setupBoard()

	"""
	Initializes a new board with the features of the crossword
	"""
	def _setupBoard(self):
		self._board = np.chararray((self._crossword.getRows(),
			self._crossword.getCols()))
		self._board[:] = CROSSWORD_CELL_EMPTY
		# fill with variables
		for var in self._crossword.getVariables():
			word = np.chararray((var[0],))
			word[:] = CHAR_UNKNOWN
			if var[1] == ORIENT_HOR:
				self._board[var[2][0],][var[2][1]:var[2][1]+var[0]] = word
			else:
				self._board[:,var[2][1]][var[2][0]:var[2][0]+var[0]] = word

	"""
	Starts the printer, printing the initial empty crossword that will be
	filled
	"""
	def start(self):
		sys.stdout.write(str(self))
		# save cursor
		sys.stdout.write("\033[s")

	"""
	Updates the given variable, setting its value to the given string
	"""
	def updateVariable(self,variable,value):
		# board at cursor
		sys.stdout.write("\033[%dA"%(self._crossword.getRows()*2-2*variable[2][0]))
		sys.stdout.write("\033[%dC"%(2+variable[2][1]*4))
		# write variable
		for letter in value:
			sys.stdout.write(letter)
			if variable[1] == ORIENT_HOR:
				sys.stdout.write("\033[%dC"%(self._spacing*2+1))
			else:
				sys.stdout.write("\033[1D\033[%dB"%(2))
		# restore cursor position
		sys.stdout.write("\033[u")

	"""
	Prints the assigned value list with the update function
	"""
	def updateSolution(self,avl):
		variables = self._crossword.getVariables()
		for i in range(len(avl)):
			self.updateVariable(variables[i],"".join(list(map(chr,avl[i]))))

	"""
	Prints the solution all at once, no start & stop
	"""
	def printSolution(self,avl):
		self.start()
		self.updateSolution(avl)

	"""
	Returns the current board as a string
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
