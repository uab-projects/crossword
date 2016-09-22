#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Loads the crossword into a list of lists with each item being a line of the
crossword

@param  filename    file to load
@return crossword loaded
"""
def loadCrossword(filename):
    crossword = [line.rstrip('\n') for line in open(filename, 'r')]
    crossword = list(map(lambda x: x.split("\t"),crossword))
    return crossword

"""
Loads the wordlist into a list given the name of the file where is stored the
dictionary

The dictionary must be formated with one word per line. Thanks :)

@param  filename    file to load
@return wordlist as a list of strings (words)
"""
def loadWordlist(filename):
    return [line.rstrip('\n') for line in open(filename, 'r')]
