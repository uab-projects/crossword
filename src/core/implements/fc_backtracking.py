from ..algorithms.backtracking import *
from itertools import compress
import sys

class CrosswordForwardCheckingBacktracking(object):
	"""
	Class attributes:

	@attr 	_domain       domain that each variable can have
	@attr 	_constraints  constraints the algorithm must apply to get a valid
	                      solution
	@attr 	_isSearching  protects the algorithm from being called twice
	                      if the value is true, no more calls are allowed
	"""
	__slots__ = ["_domain","_constraints","_navl","_isSearching"]

	"""
	Initializes a new backtracking algorithm with the given domain to set into
	the variables

	@param 	domain       domain of the variables
	@param 	constraints  constraints to apply in the problem
	"""
	def __init__(self, domain, constraints):
		self._domain = domain
		self._constraints = constraints
		self._isSearching = False

	"""
	Starts the backtracking algorithm given the unassigned variables that the
	algorithm will have to fill using the backtracking private function

	If you call the algorithm while it's already searching, an assertion
	will raise

	@param 		navl		not assigned variables list that must be filled
	@return 	assigned variables list or None if no solution could be found
	"""
	def __call__(self, navl):
		assert not self._isSearching
		self._isSearching = True
		navl = self._sortByConstraintsNumber(self._transformNavl(navl))
		avl = [None for _ in range(len(navl))]
		domains = self._transformDomains(navl)
		sol = self.__backtracking(avl,navl,domains)
		self._isSearching = False
		return sol

	"""
	Transforms data to be prepared for the algorithm

	@param 	navl 	unassigned variable list as list of strings
	@return navl 	where each item is a tuple setting the reference to the
	original variable and its length [(index,len),...]
	"""
	def _transformNavl(self,navl):
		navl = list(map(lambda i: (i,len(navl[i])), range(len(navl))))
		return navl

	"""
	Sorts the navl variables according to the number of restrictions they have
	in order to then pick variables smartly
	"""
	def _sortByConstraintsNumber(self,navl):
		constraints_per_var = list(map(lambda x: len(x),self._constraints))
		new_navl = []

		while len(constraints_per_var):
			max_constraints = max(constraints_per_var)
			max_index = constraints_per_var.index(max_constraints)
			constraints_per_var.pop(max_index)
			new_navl.append(navl[max_index])
			navl.pop(max_index)

		return new_navl

	"""
	Defines the backtracking algorithm basic implementation, given the list of
	variables to assign and the already assigned variable, recurses it self
	to search over the decision tree until it finds a valid assignation of
	variables into values of the domain that satisfy the constraints.

	After that, returns the solution, this means, the assigned variables or
	None if no result could be found

	@param	avl		assigned variables list, list of variables assigned
	@param 	navl 	not assigned variables list, list of variables that must be
					assigned
	@return avl with the solution or None if no solution could be found
	"""
	def __backtracking(self, avl, navl, domains):
		# Check if finished assignations
		if not navl:
			return avl
		# Get variable to assign and its domain
		variable = self._chooseVariableToAssign(navl)
		variableDomain = self._getDomainForVariable(variable,domains)
		# Loop over the possibilities of the domain
		for asignableIndex in variableDomain:
			asignableValue = self._domain[variable[0]][asignableIndex]
			if self._satisfiesConstraints(avl, variable, asignableValue):
				self._updateDomain(var, constraints,inserted_constraints,domains,False)
				if domains != None:
					avl[variable[0]]=asignableValue
					solution = self.__backtracking(avl,
						self._removeVariableToAssign(navl,variable),
						domains)
					if self._isCompleteSolution(solution):
						return solution
					else:
						avl[variable[0]] = None
						self._updateDomain(var,constraints,inserted_constraints,domains,True)
		return None

	"""
	Allows to define a function that will be called to assign the variable to
	try to assign from the list of unassigned variables

	@param	navl	not assigned variable list
	@return	a variable that has to be assigned
	"""
	def _chooseVariableToAssign(self, navl):
		return navl[0] # This is fucking temporary dear Carlos

	"""
	If the variable has been correctly assigned, we must remove them from the
	variables to assign, this method has to remove the variable passed from
	the list of variables to assign (navl)

	@param 	navl 		not assigned variable list
	@param 	variable 	variable that has been assigned and must be returned
	@return navl without variable in it
	"""
	def _removeVariableToAssign(self, navl, variable):
		return navl[1:]

	"""
	Given a variable that must be assigned, returns the domain that the variable
	can have in order to iterate over its possibilities

	@param 	variable		variable that we have to assign
	@return list with the values of the domain that the variable can have
	"""
	def _getDomainForVariable(self,variable,domains):
		return compress(range(len(domains[variable[0]],variable[0])))

	"""
	Given a variable and it's supposed value assignation, checks if assigning
	the variable to the value satisfies all constraints

	@param	variable 	variable to assign
	@param 	value 		value to assign to the variable
	"""
	def _satisfiesConstraints(self, avl, variable, value):
		constraints = self._constraints[variable[0]]
		for constraint in constraints:
			constrained_word = constraint[1]
			if avl[constrained_word] == None:
				continue
			elif avl[constrained_word][constraint[2]] != value[constraint[0]]:
				return False
		return True

	"""
	Checks if the list of assigned values contain a valid solution for the
	problem, in other words, the assigned values satisfies all constraints

	@param 	avl 		assigned variables list
	@return True if a complete solution, False if not
	"""
	def _isCompleteSolution(self,avl):
		return avl != None

	"""

	"""
	def _forwardChecking():
		return False

	"""

	"""
	def _updateDomain(self, var, constraints, inserted_constraints, domains, val):
		for constraint_ref in inserted_constraints:
			constrained_var = constraint_ref[0]
			constraint = constraints[constrained_var][constraint_ref[1]]
			for i in domains[constrained_var]:
				if self._domain[var[1]][i][constraint[0]] != constraint[1]:
					domains[constrained_var][i] = val


	def _transformDomains(self,navl):
		new_domains = [[] for _ in range(len(navl))]
		for var in navl:
			new_domains[var[0]] = [True for _ in range(len(self._domain[var[1]]))]
		return new_domains
