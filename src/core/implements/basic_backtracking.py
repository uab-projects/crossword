from ..algorithms.backtracking import *
import sys
class CrosswordBasicBacktracking(object):
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
		navl = self._transformNavl(navl)
		avl = [None for _ in range(len(navl))]
		sol = self.__backtracking(avl,navl)
		self._isSearching = False
		return sol

	"""
	Transforms data to be prepared for the algorithm
	"""
	def _transformNavl(self,navl):
		navl = list(map(lambda i: (i,len(navl[i])), range(len(navl))))
		return navl

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
	def __backtracking(self, avl, navl):
		# Check if finished assignations
		if not navl:
			return avl
		# Get variable to assign and its domain
		variable = self._chooseVariableToAssign(navl)
		variableDomain = self._getDomainForVariable(variable)
		# Loop over the possibilities of the domain
		for asignableValue in variableDomain:
			if self._satisfiesConstraints(avl, variable, asignableValue):
				avl[variable[0]]=asignableValue
				solution = self.__backtracking(avl,
					self._removeVariableToAssign(navl,variable))
				if self._isCompleteSolution(solution):
					return solution
				else:
					avl[variable[0]] = None
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
	def _getDomainForVariable(self,variable):
		return self._domain[variable[1]]

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
