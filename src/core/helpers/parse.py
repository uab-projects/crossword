"""
Checks if the given argument is a valid integer number. If it returns true, then
you can safely use int(num) to parse it to an integer, otherwise you'll get a
ValueError exception

@paramm 	num 	number to parse
@return 	True if num is a valid integer
"""
def isInteger(num):
	try:
		int(num)
		return True
	except ValueError:
		return False
