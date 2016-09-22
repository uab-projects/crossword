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
Converts the crossword into a list of unassigned variables
"""

"""
Loads the wordlist into a list given the name of the file where is stored the
dictionary

The dictionary must be formated with one word per line. Thanks :)

@param  filename    file to load
@return wordlist as a list of strings (words)
"""
def loadWordList(filename):
    return [line.rstrip('\n') for line in open(filename, 'r')]

"""

@param wordlist a list contaning all the words
@return formatWordList a list where each element is a list contaning
        the same length words, one list for each word  length
"""
def formatWordList(wordlist):
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

    return formattedWordList
