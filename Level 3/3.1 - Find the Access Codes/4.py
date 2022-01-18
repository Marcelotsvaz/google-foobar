from collections import defaultdict
from itertools import chain



def solution( numbers ):
	'''
	First we get all pairs of indices `i1` and `i2` such as `numbers[i2] % numbers[i1] == 0` and `i1 < i2`.
	Since the list could be unsorted and there's repeated elements we'll need the indices.
	
	For [ 1, 2, 3, 4, 5, 6 ] we should get:
	
	allMultiples = {
		0: [ 1, 2, 3, 4, 5 ],
		1: [ 3, 5 ],
		2: [ 5 ],
	}
	
	Then we match the pairs using the indices to find the triples.
	
	A lucky triple `( numbers[i1], numbers[i2], numbers[i3] )` is valid if both `i2 in allMultiples[i1]` and
	`i3 in allMultiples[i2]` are true.
	
	Finding the triples in two steps give us O(n^2), instead of O(n^3) with a triple-nested loop.
	But that comes at the cost of raising the space complexity (including the input) from O(n) to O(n^2).
	'''
	
	# Get all pairs.
	allMultiples = defaultdict( list )
	for i1, n1 in enumerate( numbers ):
		for i2, n2 in enumerate( numbers[ i1 + 1 : ] ):
			if n2 % n1 == 0:
				allMultiples[i1].append( i2 + i1 + 1 )
	
	# Count triples from the pairs.
	luckyTriplesCount = 0
	for i2 in chain.from_iterable( allMultiples.values() ):
		luckyTriplesCount += len( allMultiples.get( i2, [] ) )
	
	return luckyTriplesCount



# print( solution( [ 1, 2, 3, 4, 5, 6 ] ) == 3 )
# print( solution( [ 1, 1, 1 ] ) == 1 )



import time
import random

samples1 = sorted( random.choices( range( 1, 1000 ), k = 20000 ) )
samples2 = sorted( random.choices( range( 1, 10000 ), k = 20000 ) )

startTime = time.time()
print( f'Triples: {solution( samples1 )}' ) 
firstTime = time.time() - startTime
firstTime *= 10**3
print( f'First: {firstTime : .0f}ms\n' )

startTime = time.time()
print( f'Triples: {solution( samples2 )}' ) 
secondTime = time.time() - startTime
secondTime *= 10**3
print( f'Second: {secondTime : .0f}ms\n' )

print( f'Ratio: {secondTime / firstTime : .3f}' )