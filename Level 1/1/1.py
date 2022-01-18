def solution( x, y ):
	'''
	Return the only element present in one list but not in the other.
	'''
	
	return set( x ).symmetric_difference( y ).pop()