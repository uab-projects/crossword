# Libraries
from core.data.constants import *

# Itemset related
"""
Itemset with small crossword + small dictionary
"""
ITEMSET_SMALL = {"name":"small",
	"crossword":CROSSWORD_FILES[0],
	"wordlist":WORDLIST_FILES[0]}

"""
Itemset with big crossword + big dictionary
"""
ITEMSET_BIG = {"name":"big",
	"crossword":CROSSWORD_FILES[1],
	"wordlist":WORDLIST_FILES[1]}

"""
Default itemset if not specified
"""
ITEMSET_DEFAULT = ITEMSET_SMALL

"""
Mapping by names of itemsets
"""
ITEMSET_BYNAME = {
	ITEMSET_SMALL["name"]: ITEMSET_SMALL,
	ITEMSET_BIG["name"]: ITEMSET_BIG
}

# Information related
"""
Shows information about the crossword given
"""
SHOW_CROSSWORD_DEFAULT = False

"""
Shows information about the wordlist given
"""
SHOW_WORDLIST_DEFAULT = False

"""
Shows the solution to the output
"""
SHOW_SOLUTION_DEFAULT = True

# Algorithm variations
"""
Chooses the simple implementation of the backtracking algorithm
"""
ALG_BACKTRACKING_SIMPLE = "backtracking"

"""
Chooses the bactracking algorithm with forward checking
"""
ALG_BACKTRACKING_FC = "forwardchecking"

"""
Default algorithm
"""
ALG_DEFAULT = ALG_BACKTRACKING_FC

# Profiling
"""
Show timers
"""
TIMERS_DEFAULT = 0
