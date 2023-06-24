from typing import Self
from collections import Counter, defaultdict
from itertools import chain
from random import choice



GridAsLists = list[list[bool]]



class Grid:
	def __init__( self, gridAsInt: int, width: int, height: int ) -> None:
		self.width = width
		self.height = height
		self.gridAsInt = gridAsInt
	
	
	def __eq__( self, value: Self ) -> bool:
		return self.width == value.width and self.height == value.height and self.gridAsInt == value.gridAsInt
	
	
	def __getitem__( self, key: tuple[int, int] ) -> bool:
		return bool( self.gridAsInt & 1 << self.width * key[1] + key[0] )
	
	
	def __setitem__( self, key, value: tuple[int, int] ) -> None:
		if value:
			self.gridAsInt |= 1 << self.width * key[1] + key[0]
		# else:
		# 	self.gridAsInt |= 1 << self.width * key[1] + key[0]
	
	
	@classmethod
	def fromLists( cls, gridAsLists: GridAsLists ) -> Self:
		width = len( gridAsLists[0] )
		height = len( gridAsLists )
		
		# Convert to integer representation.
		grid = cls( 0, width, height )
		for y in range( height ):
			for x in range( width ):
				grid[x, y] = gridAsLists[y][x]
		
		return grid
	
	
	def asLists( self ) -> GridAsLists:
		'''
		
		'''
		
		return [
			[
				self[x, y]
				for x in range( self.width )
			]
			for y in range( self.height )
		]
	
	
	def __str__( self ) -> str:
		green = '\033[42m'
		reset = '\033[0m'
		
		lines = [ '🮀🮀' * self.width ]
		columns = []
		for y in range( self.height ):
			for x in range( self.width ):
				if self[x, y]:
					columns.append( green + '🭼🭿' + reset )
				else:
					columns.append( '🭼🭿' )
			
			lines.append( ''.join( columns ) )
			columns.clear()
		
		return '\n'.join( lines )
	
	
	def nextGrid( self ) -> Self:
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
	def solutions( self ) -> list[Self]:
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
	
	
	def sliceVertical( self, x: int ) -> Self:
		gridSlice = self.__class__( 0, 1, self.height )
		
		for y in range( self.height ):
			gridSlice[0, y] = self[x, y]
		
		return gridSlice
	
	
	def sliceHorizontal( self, y: int ) -> Self:
		gridSlice = self.__class__( 0, self.width, 1 )
		
		for x in range( self.width ):
			gridSlice[x, 0] = self[x, y]
		
		return gridSlice
	
	
	def columnSolutions( self, x: int ) -> list[Self]:
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
						newColumnSolution = columnSolution[:]
						newColumnSolution.append( cellSolution )
						nextSolutionsByKey[bottom].append( newColumnSolution )
			
			solutionsByKey = nextSolutionsByKey
		
		newColumnSolutions = []
		for columnSolution in chain.from_iterable( solutionsByKey.values() ):
			newColumnSolution = self.__class__( 0, 2, self.height + 1 )
			
			for y, cellSolution in enumerate( columnSolution ):
				newColumnSolution[0, y] = cellSolution[0, 0]
				newColumnSolution[1, y] = cellSolution[1, 0]
				
				newColumnSolution[0, y + 1] = cellSolution[0, 1]
				newColumnSolution[1, y + 1] = cellSolution[1, 1]
			
			newColumnSolutions.append( newColumnSolution )
		
		return newColumnSolutions
	
	
	def solve( self ) -> int:
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
		
		return solutionCounter.total()



t0 = [
	[
		[ False ],
		[ True ],
		[ False ],
	],
	2,
]

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
	
	print( f'Test {index}: ', end = '' )
	if results == test[1]:
		print( f'success!' )
	else:
		print( f'faileds! Returned {results} instead of {test[1]}.' )



# import timeit
# time = timeit.timeit( lambda: Grid.fromLists( t4[0] ).solve(), number = 100 ) / 100
# print( f' Result: {time:,.3f}s' )



# import sys
# import trace
# tracer = trace.Trace(
#     ignoredirs = [ sys.prefix, sys.exec_prefix ],
#     trace = 0,
#     count = 1,
# )
# tracer.run( 'Grid.fromLists( t4[0] ).solve()' )
# r = tracer.results()
# r.write_results( show_missing = True, coverdir = '.' )



# Column results:
# 50x9 (All True): 78s
# 50x9 (All False): 243s
# 50x9 (Random): 108s

# Cell results:
# 50x9 (All True): 0.057s
# 50x9 (All False): 91s
# 50x9 (Random): 1.391s



# TODO:
# Symmetry on 1-slice?