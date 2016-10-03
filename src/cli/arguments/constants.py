# Itemset related
"""
Itemset with small crossword + small dictionary
"""
ITEMSET_SMALL = "small"

"""
Itemset with big crossword + big dictionary
"""
ITEMSET_BIG   = "big"

"""
Default itemset if not specified
"""
ITEMSET_DEFAULT = ITEMSET_SMALL

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
