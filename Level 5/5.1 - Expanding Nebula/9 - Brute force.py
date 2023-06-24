# This will take literaly 1000 years...
def solution( nextGrid ):
	nextWidth = len( nextGrid[0] )
	nextHeight = len( nextGrid )
	width = nextWidth + 1
	height = nextHeight + 1
	solutions = 0
	
	
	# Convert grid to integer.
	nextGridInt = 0
	for y in range( nextHeight ):
		for x in range( nextWidth ):
			if nextGrid[y][x]:
				nextGridInt |= 1 << nextWidth * y + x
	
	# Iterate all solutions.
	print( 2 ** ( width * height ) )
	for gridInt in range( 2 ** ( width * height ) ):
		for y in range( nextHeight ):
			for x in range( nextWidth ):
				cell = sum( [
					bool( gridInt & 1 << width * y + x ),
					bool( gridInt & 1 << width * y + x + 1 ),
					bool( gridInt & 1 << width * ( y + 1 ) + x ),
					bool( gridInt & 1 << width * ( y + 1 ) + x + 1 ),
				] ) == 1
				
				if cell != bool( nextGridInt & 1 << nextWidth * y + x ):
					break
			else:
				continue
			
			break
		else:
			solutions += 1
	
	return solutions