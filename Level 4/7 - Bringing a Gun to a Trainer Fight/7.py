from collections import defaultdict
try:
	from math import gcd
except ImportError:
	# Python 2. =(
	from fractions import gcd as gcd2
	gcd = lambda x, y: abs( gcd2( x, y ) )



def project( position, size, i, j ):
	'''
	Return the position of a point mirrored `n` times and
	shifted by `n * size`, independently on both axis.
	'''
	
	x = i * size[0] + ( -1 )**( i % 2 ) * position[0] % size[0]
	y = j * size[1] + ( -1 )**( j % 2 ) * position[1] % size[1]
	
	return ( x, y )



def normalize( origin, target ):
	'''
	Normalize an integer vector by dividing its components by their greatest common divisor.
	'''
	
	x = target[0] - origin[0]
	y = target[1] - origin[1]
	
	divisor = gcd( x, y ) or 1	# `or 1` covers direction ( 0, 0 ).
	
	return ( x // divisor, y // divisor )



def distanceSquared( a, b ):
	'''
	Return the distance between two points.
	'''
	
	dx = b[0] - a[0]
	dy = b[1] - a[1]
	
	return dx * dx + dy * dy



def solution( roomSize, myPosition, trainerPosition, weaponRange ):
	'''
	Find the number of unique directions that point towards `trainerPosition` without going through `myPosition`.
	
	We can figure out the path the beam will take after being reflected by successively mirroring the room every time
	the beam hits a wall, instead of mirroring the beam itself. Therefore, we can find all possible paths by iterating
	over all projected trainers within `weaponRange`.
	
	The time complexity is `O( weaponRange^2 / ( roomSize[0] * roomSize[1] ) )`, which is linear in relation to the
	number of projected rooms.
	'''
	
	# Projected rooms we'll need to check, rounded away from zero.
	iMin = ( -weaponRange + myPosition[0] ) // roomSize[0]
	iMax = -( -( weaponRange + myPosition[0] ) // roomSize[0] )
	
	jMin = ( -weaponRange + myPosition[1] ) // roomSize[1]
	jMax = -( -( weaponRange + myPosition[1] ) // roomSize[1] )
	
	# Since we only have integer coordinates, we'll only need floats for the distances. By keeping them squared we can
	# use integers and avoid any problems with float comparison.
	weaponRange = weaponRange**2
	
	# Get the distance to all trainer projections within range, but only the closest one in any direction.
	directions = defaultdict( lambda: float( 'inf' ) )
	for j in range( jMin, jMax + 1 ):
		for i in range( iMin, iMax + 1 ):
			trainerProjection = project( trainerPosition, roomSize, i, j )
			direction = normalize( myPosition, trainerProjection )
			dist = distanceSquared( myPosition, trainerProjection )
			
			if dist <= weaponRange and dist < directions[direction]:
				directions[direction] = dist
	
	# If one of our own projections is in the same direction of a trainer projection but closer, it means we hit
	# ourselves before the trainer, so we drop that direction.
	for j in range( jMin, jMax + 1 ):
		for i in range( iMin, iMax + 1 ):
			selfProjection = project( myPosition, roomSize, i, j )
			direction = normalize( myPosition, selfProjection )
			dist = distanceSquared( myPosition, selfProjection )
			
			if dist < directions[direction]:
				directions.pop( direction )
	
	return len( directions )



# End of submission.



print( ' 1:', solution( [ 3, 2 ], [ 1, 1 ], [ 2, 1 ], 2 ) == 1 )
print( ' 2:', solution( [ 3, 2 ], [ 1, 1 ], [ 2, 1 ], 3 ) == 3 )
print( '*3:', solution( [ 3, 2 ], [ 1, 1 ], [ 2, 1 ], 4 ) == 7 )
print( ' 4:', solution( [ 3, 2 ], [ 1, 1 ], [ 2, 1 ], 5 ) == 13 )
print( '*5:', solution( [ 300, 275 ], [ 150, 150 ], [ 151, 152 ], 500 ) == 9 )
print( ' 6:', solution( [ 300, 275 ], [ 150, 150 ], [ 151, 152 ], 10000 ) == 3809 )


import timeit
time = timeit.timeit( lambda: solution( [ 3, 2 ], [ 1, 1 ], [ 2, 1 ], 1000 ) == 397845, number = 10 ) / 10 * 10**3
print( f' 7: {time:,.0f}ms' )