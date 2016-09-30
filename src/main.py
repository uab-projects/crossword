#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
from core.data.wordlist import *
from core.data.crossword import *
from core.data.constants import *
from core.helpers.parse import *
from core.implements.basic_backtracking import *

if __name__ == "__main__":
	# Arguments parsing
	itemSet = ITEMSET_DEFAULT
	if len(sys.argv) > 1:
		# defaultItemSet
		strItemSet = sys.argv[1]
		if not isInteger(strItemSet):
			print ("ItemSet must be a number")
		elif int(strItemSet) < 0 or int(strItemSet) >= len(WORDLIST_FILES):
			print("ItemSet does not fit in the limits [%d-%d]"\
				%(0,len(WORDLIST_FILES)-1))
		else:
			itemSet = int(strItemSet)
	else:
		print("Using default args")
	# Load data
	print("Loading data...")
	time_load_start = time.time()
	# Wordlist
	wordlist = WordList(WORDLIST_FILES[itemSet])
	time_load_wordlist_start = time.time()
	wordlist.read()
	print("Wordlist read in %f seconds"%(time.time()-\
		time_load_wordlist_start))
	time_load_wordlist_start_parse = time.time()
	wordlist.parse()
	print("Wordlist parsed in %f seconds"%(time.time()-\
		time_load_wordlist_start_parse))
	print("Wordlist loaded in %f seconds"%(time.time()-\
		time_load_wordlist_start))
	if "--wordlist" in sys.argv:
		print(wordlist)
	# Crossword
	crossword = Crossword(CROSSWORD_FILES[itemSet])
	time_load_crossword_start = time.time()
	crossword.read().parse()
	time_load_crossword_end = time.time()
	print("Crossword loaded in %f seconds"%(time_load_crossword_end-\
		time_load_crossword_start))
	if "--crossword" in sys.argv:
		print(crossword)
	# Loading ended
	time_load_end = time.time()
	print("Ended loading data (spend %f seconds)"%(\
		time_load_end-time_load_start))
	print("Starting Bactracking algorithm...")
	time_alg_start = time.time()
	# Choose algorithm
	if "--backtracking" in sys.argv or True:
		solver = CrosswordBasicBacktracking(wordlist.getList(),
			crossword.getConstraints())
	else:
		solver = CrosswordForwardCheckingBacktracking(wordlist.getList(),
			crossword.getConstraints())
	solution = solver(crossword.getVariables())
	time_alg_end = time.time()
	print("Ended backtracking algorithm (spent %f seconds)"%(\
		time_alg_end-time_alg_start))
	#print(solution)
	if(solution != None):
		for row in crossword.applyVariables(solution):
			for col in row:
				print(col+" ",end="")
			print("")
	else:
		print("You are a fail, and the algorithm too")
	print("Total time: %f seconds"%(time_alg_end-time_load_start))
