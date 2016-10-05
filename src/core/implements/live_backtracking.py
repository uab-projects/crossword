from ..algorithms.backtracking import *
from itertools import compress
import sys
import numpy as np
import core.data.constants as constants
import logging

LOGGER = logging.getLogger(__name__)


class CrosswordLiveBacktracking(object):
	"""
	Class attributes:

	@attr 	_domain       domain that each variable can have
	@attr 	_constraints  constraints the algorithm must apply to get a valid
	                      solution
	@attr 	_isSearching  protects the algorithm from being called twice
	                      if the value is true, no more calls are allowed
	@attr 	_variables 	  variables obtained from crossword
	@attr 	_tries        tries by variable
	@attr   _totalTries   total number of tries
	"""
	__slots__ = ["_domain","_constraints","_isSearching","_variables",
	"_printer","_tries","_totalTries"]

	"""
	Initializes a new backtracking algorithm with the given domain to set into
	the variables

	@param 	domain       domain of the variables
	@param 	constraints  constraints to apply in the problem
	@param 	printer 	printer
	"""
	def __init__(self, domain, constraints, printer):
		self._domain = domain
		self._constraints = constraints
		self._printer = printer
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
		# Saving status of the algorithm
		self._isSearching = True
		self._variables = navl
		# Initializing variables
		navl = self._sortByConstraintsNumber(self._getNavl())
		print("Current NAVL before reordering is: \n", navl)
		#Reordering the navl in order to speedup the application
		navl = self._reorderNAVL(navl[1:],[navl[0]],navl[0])
		print("Current NAVL after reordering is: \n", navl)
		constraints = [[] for _ in range(len(navl))]
		domains = self._getDomains()
		avl = [None for _ in range(len(navl))]
		self._tries = np.zeros(len(self._variables),dtype=np.uint32)
		self._totalTries = 0
		# Call backtracking
		self._printer.start()
		sol = None
		try:
			sol = self.__backtracking(avl, navl, constraints, domains, None)
		except KeyboardInterrupt as e:
			self._printer.stop()
			LOGGER.error("User interrupted the algorithm")
		if sol != None:
			self._printer.updateSolution(sol)
		self._printer.stop()
		self._isSearching = False
		return sol

	"""
	Reads the variables assigned to the object to be solved and generate a list
	of unassigned variables in the following format
	 [var_0,var_1,var_2,...]
	where var_i is a tuple (index,len) that tells the variable index and the
	length of that variable

	@return 	navl list
	"""
	def _getNavl(self):
		return list(map(lambda i: (i,self._variables[i][0]),
		range(len(self._variables))))

	"""
	Reads the variables assigned to the object that have to be solved and
	looks in the domain for the words that fit it each variables length so it
	generates an all True vector for each variable

	@return 	domains list
	"""
	def _getDomains(self):
		return [np.ones(len(self._domain[var[0]]),dtype=np.bool)
			for var in self._variables]

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
	Sorts the navl variables according to the number of restrictions and
	intersections they have between them in order to then pick variables
	even smartly than before

	@param	navl		not assigned remaining variable list
	@param 	new_navl	not assigned picked variable list
	@param	variable	variable selected to be filled in the next iteration
	@return	navl		new not assigned variable list with the new order

	"""
	def _reorderNAVL(self, navl, new_navl, variable):
		if not navl:
			return new_navl
		else:
			max_constraints, var = 0, navl[0]
			applicants = self._constraints[variable[0]]
			for app in applicants:
				current_constraints, length = len(self._constraints[app[1]]), self._variables[app[1]][0]
				candidate = (app[1], length)

				if (current_constraints > max_constraints) and (candidate in navl):
					max_constraints, var = current_constraints, candidate

			#New assignments
			new_navl.append(var)
			index = navl.index(var)
			navl = navl[:index] + navl[index+1:]

			self._reorderNAVL(navl, new_navl, var)

			return new_navl

	"""
	Returns the next varaible to fill. That variable is the one who has less
	domain values remaining.

	@param	navl		not assigned remaining variable list
	@param	prevar		variable selected in the previous iteration
	@return	variable	variable to be filled in the current iteration
	"""
	def _nextVarByDomainValuesRemaining(self, navl, domains, prevar):
		if not prevar:
			return navl[0]

		variable = navl[0]
		minimum_domain_values = np.sum(domains[variable[0]])

		for var in navl[1:]:
			current_domain_values = np.sum(domains[var[0]])

			if current_domain_values < minimum_domain_values:
				variable = var
				minimum_domain_values = current_domain_values
		return variable

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
	def __backtracking(self, avl, navl, constraints, domains, prevar, prof=0):
		# Check if finished assignations
		if not navl:
			return avl
		# Get variable to assign and its domain
		# variable = self._chooseVariableToAssign(navl)
		variable = self._nextVarByDomainValuesRemaining(navl, domains, prevar)

		variableDomain = self._getDomainForVariable(variable, domains)
		# Loop over the possibilities of the domain
		for asignableIndex in variableDomain:
			asignableValue = self._domain[variable[1]][asignableIndex]
			self._totalTries += 1
			self._tries[variable[0]] += 1
			self._printer.updateVariable(self._variables[variable[0]],
			asignableValue,
				"""Variable:    INDEX    = %-6d | REAL  = %s%-5d | LENGTH = %-6d | POS = %s\n"""
				"""Domain:      SIZE     = %-6d | VALID = %-6d | TRIED  = %-6d |\n"""
				"""Constraints: CURRENT  = %-6d | TOTAL = %-6d | LAST   = %-6s | \n"""
				"""Status:      ASSIGNED = %02d/%02d  | TRIES = %-6d | DEPTH  = %-6d |"""%(\
					# variables
					variable[0],
					"H" if self._variables[variable[0]][1] \
						== constants.ORIENT_HOR else "V",
					self._variables[variable[0]][2],
					variable[1],
					str(self._variables[variable[0]][3]),
					# domain
					domains[variable[0]].shape[0],
					np.sum(domains[variable[0]]),
					self._tries[variable[0]],
					# constraints,
					len(constraints[variable[0]]),
					len(self._constraints[variable[0]]),
					"Empty" if not len(constraints[variable[0]]) \
						else str(constraints[variable[0]][-1]),
					# status
					len(self._variables)-len(navl),
					len(self._variables),
					self._totalTries,
					prof
			))
			if self._satisfiesConstraints(constraints, avl, variable,
			asignableValue):
				avl[variable[0]]=asignableValue
				new_constraints = self._updateConstraints(constraints, variable,
				asignableValue)
				new_domains = self._updateDomains2(constraints, new_constraints,
				domains)
				valid_domains = self._checkDomains(domains)
				if valid_domains:
					solution = self.__backtracking(avl,
					self._removeVariableToAssign(navl, variable), constraints,
					new_domains, variable, prof+1)
				if valid_domains and self._isCompleteSolution(solution):
					return solution
				else:
					avl[variable[0]] = None
					self._removeFromConstraints(new_constraints, constraints)

		return None

	"""
	Given the current dynamic constraints, the constraints that have just been
	inserted, and the current domains, returns domains that are restricted
	according to the inserted constraints

	@param 	constraints 	dynamic constraints in the current state
	@param 	new_constraints	inserted constraints references with the new
							assigned value
	@param 	domains 		current domains to restrict
	@return list of new domains representing constraints applied
	"""
	def _updateDomains(self, constraints, new_constraints, domains):
		# New domains to represent constraints
		new_domains = [np.array(domain,copy=True) for domain in domains]
		# Apply constraints
		for constraint_ref in new_constraints:
			constraint = constraints[constraint_ref[0]][constraint_ref[1]]
			new_domains[constraint_ref[0]] *= np.where(
				self._domain[self._variables[constraint_ref[0]][0]]
				[:,constraint[0]] == constraint[1],True,False)
		return new_domains

	def _updateDomains2(self, constraints, new_constraints, domains):
		# New domains to represent constraints
		new_domains = [np.array(domain,copy=True) for domain in domains]
		# Apply constraints
		for variable_i in range(len(self._variables)):
			for constraint in constraints[variable_i]:
				new_domains[variable_i] *= np.where(
					self._domain[self._variables[variable_i][0]][:,constraint[0]] ==\
					constraint[1],True,False)
		return new_domains

	def _checkDomains(self, domains):
		for dom in domains:
			if not any(dom):
				return False
		return True

	"""
	Allows to remove constraints that are considered not viable from the list
	once it's known that the variable it's not part of the solution

	@param update_list 		list with information of recent updates to constraints
	@param constraints 		list of constraints
	@param var 				variable we tried to assign
	"""
	def _removeFromConstraints(self, update_list, constraints):
		for item in update_list:
			constraints[item[0]].pop(item[1])

	"""
	Allows to define a function that will be called to assign the variable to
	try to assign from the list of unassigned variables

	@param	navl	not assigned variable list
	@return	a variable that has to be assigned
	"""
	def _chooseVariableToAssign(self, navl):
		return navl[0]

	"""
	If the variable has been correctly assigned, we must remove them from the
	variables to assign, this method has to remove the variable passed from
	the list of variables to assign (navl)

	@param 	navl 		not assigned variable list
	@param 	variable 	variable that has been assigned and must be returned
	@return navl without variable in it
	"""
	def _removeVariableToAssign(self, navl, variable):
		index = navl.index(variable)
		navl = navl[:index] + navl[index+1:]
		return navl

	"""
	Given a variable that must be assigned, returns the domain that the variable
	can have in order to iterate over its possibilities

	@param 	variable		variable that we have to assign
	@return list with the values of the domain that the variable can have
	"""
	def _getDomainForVariable(self,variable,domains):
		#return self._domain[variable[1]]
		return compress(range(len(domains[variable[0]])),domains[variable[0]])

	def _updateConstraints(self,constraints, var, value):
		i = var[0]
		update_list=[]
		st_constraints = self._constraints[i]
		for const in st_constraints:
			constraints[const[1]].append((const[2],value[const[0]]))
			update_list.append((const[1], len(constraints[const[1]])-1))
		return update_list

	"""
	Given a variable and it's supposed value assignation, checks if assigning
	the variable to the value satisfies all constraints

	@param	variable 	variable to assign
	@param 	value 		value to assign to the variable
	"""
	def _satisfiesConstraints(self, constraints, avl, var, value):
		constraints_var = constraints[var[0]]
		for constraint in constraints_var:
			if value[constraint[0]] != constraint[1]:
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
