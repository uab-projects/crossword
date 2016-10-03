#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Libraries
import sys
import time
import logging

# Modules
from core.data.wordlist import *
from core.data.crossword import *
from core.data.constants import *
from core.helpers.parse import *
from core.implements.basic_backtracking import *
from core.implements.fc_backtracking import *
import core.log
from cli.arguments.parsers import DEFAULT_PARSER
from cli.arguments.constants import *


# Constants
LOGGER = logging.getLogger(__name__)

# Functions
"""
Takes the system arguments vector and tries to parse the arguments in it given
the argument parser specified and returns the namespace generated

@param 	parser 	the ArgumentParser objects to use to parse the arguments
"""
def parseArguments(parser):
	return parser.parse_args()

"""
Given the origin of the data for the wordlist, loads the wordlist and returns
it, while giving some information about it if it's required

@param 	origin 	the source to load the wordlist from
@return wordlist valid object (or None if couldn't load)
"""
def loadWordlist(origin):
	LOGGER.info("-> Loading wordlist")
	wordlist = WordList(origin)
	if args.timers > 1: 	time_load_wordlist_start = time.time()
	wordlist.read()
	if args.timers > 2:
		LOGGER.info("--> Read   in %f seconds",time.time()-\
		time_load_wordlist_start)
		time_load_wordlist_start_parse = time.time()
	wordlist.parse()
	if args.timers > 2:
		LOGGER.info("--> Parsed in %f seconds",time.time()-\
		time_load_wordlist_start_parse)
	if args.timers > 1:
		LOGGER.info("--> Loaded in %f seconds",time.time()-\
		time_load_wordlist_start)
	if args.show_wordlist:
		LOGGER.info(wordlist)
	return wordlist

"""
Given the origin of the data for the crossword, loads the crossword and returns
it, while giving some information about it if it's required

@param 	origin 	the source to load the wordlist from
@return crossword valid object (or None if couldn't load)
"""
def loadCrossword(origin):
	crossword = Crossword(origin)
	LOGGER.info("-> Loading crossword")
	if args.timers > 1:		time_load_crossword_start = time.time()
	crossword.read().parse()
	if args.timers > 1:
		LOGGER.info("--> Loaded in %f seconds",time.time()-\
		time_load_crossword_start)
	if args.show_crossword:
		LOGGER.info(crossword)
	return crossword

"""
Retrieves the algorithm object to use depending on the arguments

@return algorithm callable object
"""
def selectAlgorithm():
	alg = None
	if args.algorithm == ALG_BACKTRACKING_SIMPLE:
		alg = CrosswordBasicBacktracking(wordlist.getList(),
			crossword.getConstraints())
	elif args.algorithm == ALG_BACKTRACKING_FC:
		alg = CrosswordForwardCheckingBacktracking(wordlist.getList(),
			crossword.getConstraints())
	return alg

"""
Given a solution from the crossword, tries to print it over the screen, or logs
that no solution was found if necessary

@param 	solution 	solution to print
"""
def showSolution(solution):
	if solution == None:
		LOGGER.info("The algorithm hasn't found any valid solution :(")
	elif args.solution:
		for row in crossword.applyVariables(solution):
			LOGGER.info(row)
	else:
		LOGGER.info("The algorithm has found a valid solution :)")

if __name__ == "__main__":
	# Parse arguments
	args = parseArguments(DEFAULT_PARSER)

	# Welcome
	LOGGER.info("Welcome to Crossword solver")
	# Load data
	LOGGER.info("Loading crossword and wordlist")
	if args.timers > 0:		time_load_start = time.time()
	# Wordlist
	wordlist = loadWordlist(args.wordlist)

	# Crossword
	crossword = loadCrossword(args.crossword)

	# Loading ended
	if args.timers > 0:
		time_load_end = time.time()
		LOGGER.info("Loaded all in %f seconds",
		time_load_end-time_load_start)
	else:
		LOGGER.info("Loaded all data succesfully")

	# Choose algorithm
	alg = selectAlgorithm()

	# Solve the problem
	LOGGER.info("Started backtracking algorithm")
	if args.timers > 0: 	time_alg_start = time.time()
	solution = alg(crossword.getVariables())
	if args.timers > 0:
		time_alg_end = time.time()
		LOGGER.info("Ended alg. in %f seconds",
		time_alg_end-time_alg_start)
	else:
		LOGGER.info("Ended succesfully backtracking algorithm")

	# Solution
	if args.timers > 0:
		LOGGER.info("TOTAL TIME:   %f seconds",time_alg_end-time_load_start)
	showSolution(solution)
