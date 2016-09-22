#~-~ coding: utf-8 ~-~

class BacktrackingAlgorithm(object):
	"""
	Class attributes:

	@attr 	_domain      domain that each variable can have
	@attr 	_constraints constraints the algorithm must apply to get a valid
	                     solution
	"""
	__slots__ = ["_domain","_constraints"]

	"""
	Initializes a new backtracking algorithm with the given domain to set into
	the variables

	@param 	domain       domain of the variables
	@param 	constraints  constraints to apply in the problem
	"""
	def __init__(self, domain, constraints):
		self._domain = domain
		self._constraints = constraints

	"""
	Starts the backtracking algorithm given the unassigned variables that the
	algorithm will have to fill
	"""
