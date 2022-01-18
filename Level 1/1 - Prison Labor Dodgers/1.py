def solution( x, y ):
	'''
	Return the only element present in one list but not in the other.
	'''
	
	return set( x ).symmetric_difference( y ).pop()



print( solution( [ 13, 5, 6, 2, 5 ], [ 5, 2, 5, 13 ] ) == 6 )
print( solution( [ 14, 27, 1, 4, 2, 50, 3, 1 ], [ 2, 4, -4, 3, 1, 1, 14, 27, 50 ] ) == -4 )