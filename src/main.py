#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Returns the domain for the given variable

@param  var variable to get domain from
@return dom domain as list of values
"""
def getDomain(var, domain):
    dom =[]
    return dom
"""
Returns True if the assignation var / value satisfies all constraints set

@param  var  variable assigned
@param  value value assigned to that variable
@param  avl list of assigned values
@param  constraints
@return True if value assigned to variable is legit
"""
def satisfiesConstraints(var, value, avl, constraints):
    #Check things
    if (1):
        return True
    return False

"""
Checks if the solution is complete

@param  res
@return
"""
def completeSolution(res):
    #Check for complete solution
    pass
"""
Constraints can be defined as a list of tuples where each tuple means:
    being (a, b, c, d) the tuple, a and c are two words that have to have the
    same letter in position b and d respectively, in other words:
        a[b] = c[d]
"""
def backtracking(avl, navl, constraints, domain):
    if not navl return avl
    var = navl[0]
    for asignableValue in getDomain(var, domain):
        if satisfiesConstraints(var, assignableValue, avl, constraints):
            applicant = backtracking([(var, asignableValue)]+avl , navl[1:], constraints, domain)
            if completeSolution(applicant):
                return res
    return False

if __name__ == "__main__":
    loadEnvironment()
