#~-~ coding: utf-8 ~-~
from abc import ABCMeta,abstractmethod,abstractproperty

class BacktrackingAlgorithm(object):
	__metaclass__ = abc
	"""
	Class attributes:

	@attr 	_domain       domain that each variable can have
	@attr 	_constraints  constraints the algorithm must apply to get a valid
	                      solution
	@attr 	_isSearching  protects the algorithm from being called twice
	                      if the value is true, no more calls are allowed
	"""
	__slots__ = ["_domain","_constraints","_isSearching"]

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
		sol = self.__backtracking([],navl)
		self._isSearching = False
		return sol

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
		variableDomain = self._getDomain(variable)
		# Loop over the possibilities of the domain
		for asignableValue in variableDomain:
			if self._satisfiesConstraints(variable, asignableValue):
				solution = backtracking(
					[(variable, asignableValue)]+avl,
					self._removeVariableToAssign(variable))
				if self._completeSolution(solution):
					return solution
		return None

	"""
	Allows to define a function that will be called to assign the variable to
	try to assign from the list of unassigned variables

	@param	navl	not assigned variable list
	@return	a variable that has to be assigned
	"""
	@abstractmethod
	def _chooseVariableToAssign(self, navl):
		pass

	"""
	If the variable has been correctly assigned, we must remove them from the
	variables to assign, this method has to remove the variable passed from
	the list of variables to assign (navl)

	@param 	navl 		not assigned variable list
	@param 	variable 	variable that has been assigned and must be returned
	@return navl without variable in it
	"""
	@abstractmethod
	def _removeVariableToAssign(self, navl, variable):
		pass

	"""
	Given a variable that must be assigned, returns the domain that the variable
	can have in order to iterate over its possibilities

	@param 	variable		variable that we have to assign
	@return list with the values of the domain that the variable can have
	"""
	@abstractmethod
	def _getDomainForVarible(self,variable):
		pass

	"""
	Given a variable and it's supposed value assignation, checks if assigning
	the variable to the value satisfies all constraints

	@param	variable 	variable to assign
	@param 	value 		value to assign to the variable
	"""
	@abstractmethod
	def _satisfiesConstraints(self, variable, value):
		pass

	"""
	Checks if the list of assigned values contain a valid solution for the
	problem, in other words, the assigned values satisfies all constraints

	@param 	avl 		assigned variables list
	@return True if a complete solution, False if not
	"""
	@abstractmethod
	def _isCompleteSolution(self, avl):
		pass

	"""
	Returns the domain attribute assigned

	@return domain
	"""
	def getDomain(self):
		return self._domain

	"""
	Returns the constraints stored

	@return 	constraints
	"""
	def getConstraints(self):
		return self._constraints


"""
Basic implementation of the basic algorithm, where main functions are
implemented, like choosing the first variable from the navl to choose, etc...
"""
class BacktrackingBasicAlgorithm(BacktrackingAlgorithm):
	def _chooseVariableToAssign(self, navl):
		return navl[0]

	def _removeVariableToAssign(self, navl, variable):
		navl = navl[1:]
		return navl

	def _getDomainForVariable(self, variable):
		return self.getDomain()
