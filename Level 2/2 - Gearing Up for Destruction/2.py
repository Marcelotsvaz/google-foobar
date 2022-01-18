from fractions import Fraction



def solution( pegs ):
	if len( pegs ) < 2:
		return [ -1, -1 ]
	
	
	# Solve for `r1 / rn = 2`.
	pTotal = Fraction( 0 )
	for p1, p2 in zip( pegs, pegs[1:] ):
		pTotal = p2 - p1 - pTotal
	
	if len( pegs ) % 2 == 0:
		r1 = -2 * pTotal / -3
	else:
		r1 = -2 * pTotal
	
	
	# Check if resulting gear configuration is valid.
	# If rn >= 1 then r1 >= 2, so we can skip checking r1.
	r = r1
	for p1, p2 in zip( pegs, pegs[1:] ):
		r =  p2 - p1 - r
		
		if r < 1:
			return [ -1, -1 ]
	
	return [ r1.numerator, r1.denominator ]



print( solution( [4, 30, 50] ) == [12, 1] )
print( solution( [4, 30, 50, 65] ) == [14, 1] )
print( solution( [4, 17, 50] ) == [-1, -1] )
print( solution( [] ) == [-1, -1] )