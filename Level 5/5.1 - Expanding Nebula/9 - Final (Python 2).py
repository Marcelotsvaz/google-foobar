from collections import Counter, defaultdict
from itertools import chain



class Grid:
	def __init__( self, gridAsInt, width, height ):
		self.width = width
		self.height = height
		self.gridAsInt = gridAsInt
	
	
	def __eq__( self, value ):
		return self.width == value.width and self.height == value.height and self.gridAsInt == value.gridAsInt
	
	
	def __getitem__( self, key ):
		return bool( self.gridAsInt & 1 << self.width * key[1] + key[0] )
	
	
	def __setitem__( self, key, value ):
		if value:
			self.gridAsInt |= 1 << self.width * key[1] + key[0]
		# else:
		# 	self.gridAsInt |= 1 << self.width * key[1] + key[0]
	
	
	@classmethod
	def fromLists( cls, gridAsLists ):
		width = len( gridAsLists[0] )
		height = len( gridAsLists )
		
		# Convert to integer representation.
		grid = cls( 0, width, height )
		for y in range( height ):
			for x in range( width ):
				grid[x, y] = gridAsLists[y][x]
		
		return grid
	
	
	def asLists( self ):
		'''
		
		'''
		
		return [
			[
				self[x, y]
				for x in range( self.width )
			]
			for y in range( self.height )
		]
	
	
	def nextGrid( self ):
		nextWidth = self.width - 1
		nextHeight = self.height - 1
		
		nextGrid = self.__class__( 0, nextWidth, nextHeight )
		for y in range( nextHeight ):
			for x in range( nextWidth ):
				if sum( [
					self[x, y],
					self[x + 1, y],
					self[x, y + 1],
					self[x + 1, y + 1],
				] ) == 1:
					nextGrid[y, x] = True
		
		return nextGrid
	
	
	# This will take literaly 1500 years...
	def solutions( self ):
		'''
		
		'''
		
		solutionWidth = self.width + 1
		solutionHeight = self.height + 1
		solutions = []
		
		# Iterate all possible solutions.
		for possibleSolutionInt in range( 2 ** ( solutionWidth * solutionHeight ) ):
			
			possibleSolution = Grid( possibleSolutionInt, solutionWidth, solutionHeight )
			for y in range( self.height ):
				for x in range( self.width ):
					cell = sum( [
						possibleSolution[x, y],
						possibleSolution[x + 1, y],
						possibleSolution[x, y + 1],
						possibleSolution[x + 1, y + 1],
					] ) == 1
					
					if cell != self[x, y]:
						break
				else:
					continue
				
				break
			else:
				solutions.append( possibleSolution )
		
		return solutions
	
	
	def sliceVertical( self, x ):
		gridSlice = self.__class__( 0, 1, self.height )
		
		for y in range( self.height ):
			gridSlice[0, y] = self[x, y]
		
		return gridSlice
	
	
	def sliceHorizontal( self, y ):
		gridSlice = self.__class__( 0, self.width, 1 )
		
		for x in range( self.width ):
			gridSlice[x, 0] = self[x, y]
		
		return gridSlice
	
	
	def columnSolutions( self, x ):
		column = self.sliceVertical( x )
		cells = [ column.sliceHorizontal( y ) for y in range( self.height ) ]
		
		solutionsByKey = defaultdict( list )
		for cellSolution in cells[0].solutions():
			bottom = cellSolution.sliceHorizontal( 1 ).gridAsInt
			solutionsByKey[bottom].append( [ cellSolution ] )
		
		for cell in cells[1:]:
			nextSolutionsByKey = defaultdict( list )
			
			for cellSolution in cell.solutions():
				top = cellSolution.sliceHorizontal( 0 ).gridAsInt
				bottom = cellSolution.sliceHorizontal( 1 ).gridAsInt
				
				if top in solutionsByKey:
					for columnSolution in solutionsByKey[top]:
						acolumnSolution = columnSolution[:]
						acolumnSolution.append( cellSolution )
						nextSolutionsByKey[bottom].append( acolumnSolution )
			
			solutionsByKey = nextSolutionsByKey
		
		newColumnSolutions = []
		for columnSolution in chain.from_iterable( solutionsByKey.values() ):
			newColumnSolution = self.__class__( 0, 2, self.height + 1)
			
			for y, cellSolution in enumerate( columnSolution ):
				newColumnSolution[0, y] = cellSolution[0, 0]
				newColumnSolution[1, y] = cellSolution[1, 0]
				
				newColumnSolution[0, y + 1] = cellSolution[0, 1]
				newColumnSolution[1, y + 1] = cellSolution[1, 1]
			
			newColumnSolutions.append( newColumnSolution )
		
		return newColumnSolutions
	
	
	def solve( self ):
		columnSolutions = ( self.columnSolutions( x ) for x in range( self.width ) )
		
		solutionCounter = Counter( solution.sliceVertical( 1 ).gridAsInt for solution in next( columnSolutions ) )
		for solutions in columnSolutions:
			newSolutionCounter = Counter()
			
			for solution in solutions:
				left = solution.sliceVertical( 0 ).gridAsInt
				right = solution.sliceVertical( 1 ).gridAsInt
				
				if left in solutionCounter:
					newSolutionCounter[right] += solutionCounter[left]
			
			solutionCounter = newSolutionCounter
		
		return sum( solutionCounter.values() )



def solution( grid ):
	return Grid.fromLists( grid ).solve()



t1 = [
	[
		[ True, False, True ],
		[ False, True, False ],
		[ True, False, True ],
	],
	4,
]

t2 = [
	[
		[ True, True, False, True, False, True, False, True, True, False ],
		[ True, True, False, False, False, False, True, True, True, False ],
		[ True, True, False, False, False, False, False, False, False, True ],
		[ False, True, False, False, False, False, True, True, False, False ],
	],
	11567,
]

t3 = [
	[
		[ True, False, True, False, False, True, True, True ],
		[ True, False, True, False, False, False, True, False ],
		[ True, True, True, False, False, False, True, False ],
		[ True, False, True, False, False, False, True, False ],
		[ True, False, True, False, False, True, True, True ],
	],
	254,
]

t4 = [
	[
		[
			# choice( [ True, False] )
			True
			# False
			for _ in range( 50 )
		]
		for _ in range( 9 )
	],
	# -1,
	100663356,
	# 342015522530891220930318205106520120995761507496882358868830383880718255659276117597645436150624945088901216664965365050,
]



for index, test in enumerate( [ t1, t2, t3, t4 ] ):
	results = Grid.fromLists( test[0] ).solve()
	
	print( 'Test {}: '.format( index ) )
	if results == test[1]:
		print( 'success!' )
	else:
		print( 'faileds! Returned {} instead of {}.'.format( results, test[1] ) )