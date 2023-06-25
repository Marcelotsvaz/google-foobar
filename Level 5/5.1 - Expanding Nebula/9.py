from typing import Self, Iterator
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
	
	
	def __hash__( self ) -> int:
		return hash( self.gridAsInt )
	
	
	def __getitem__( self, key: tuple[int, int] ) -> bool:
		return bool( self.gridAsInt & 1 << self.height * key[0] + key[1] )
	
	
	def __setitem__( self, key, value: tuple[int, int] ) -> None:
		if value:
			self.gridAsInt |= 1 << self.height * key[0] + key[1]
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
	
	
	def singleCellSolutions( self ) -> list[Self]:
		'''
		
		'''
		
		if self.gridAsInt == 0:
			solutions = [ 0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15 ]
		else:
			solutions = [ 1, 2, 4, 8 ]
		
		return [ self.__class__( gridAsInt, 2, 2 ) for gridAsInt in solutions ]
	
	
	def sliceVertical( self, x: int ) -> Self:
		bitMask = 2 ** self.height - 1
		offset = x * self.height
		
		gridAsInt = self.gridAsInt >> offset & bitMask
		
		return self.__class__( gridAsInt, 1, self.height )
	
	
	def sliceHorizontal( self, y: int ) -> Self:
		gridSlice = self.__class__( 0, self.width, 1 )
		
		for x in range( self.width ):
			gridSlice[x, 0] = self[x, y]
		
		return gridSlice
	
	
	def columnSolutions( self, x: int ) -> Iterator[Self]:
		column = self.sliceVertical( x )
		cells = ( column.sliceHorizontal( y ) for y in range( self.height ) )
		
		solutionsByKey = defaultdict( list )
		for cellSolution in next( cells ).singleCellSolutions():
			bottom = cellSolution.sliceHorizontal( 1 )
			
			longCellSolution = self.__class__( 0, 2, self.height + 1 )
			longCellSolution[0, 0] = cellSolution[0, 0]
			longCellSolution[0, 1] = cellSolution[0, 1]
			longCellSolution[1, 0] = cellSolution[1, 0]
			longCellSolution[1, 1] = cellSolution[1, 1]
			
			solutionsByKey[bottom].append( longCellSolution )
		
		for y, cell in enumerate( cells, start = 1 ):
			nextSolutionsByKey = defaultdict( list )
			
			for cellSolution in cell.singleCellSolutions():
				top = cellSolution.sliceHorizontal( 0 )
				bottom = cellSolution.sliceHorizontal( 1 )
				
				if top in solutionsByKey:
					for columnSolution in solutionsByKey[top]:
						newColumnSolution = self.__class__( columnSolution.gridAsInt, 2, self.height + 1 )
						
						newColumnSolution[0, y + 1] = cellSolution[0, 1]
						newColumnSolution[1, y + 1] = cellSolution[1, 1]
						
						nextSolutionsByKey[bottom].append( newColumnSolution )
			
			solutionsByKey = nextSolutionsByKey
		
		return chain.from_iterable( solutionsByKey.values() )
	
	
	def solve( self ) -> int:
		columnSolutions = ( self.columnSolutions( x ) for x in range( self.width ) )
		
		solutionCounter = Counter( solution.sliceVertical( 1 ) for solution in next( columnSolutions ) )
		for solutions in columnSolutions:
			newSolutionCounter = Counter()
			
			for solution in solutions:
				left = solution.sliceVertical( 0 )
				right = solution.sliceVertical( 1 )
				
				if left in solutionCounter:
					newSolutionCounter[right] += solutionCounter[left]
			
			solutionCounter = newSolutionCounter
		
		return solutionCounter.total()



t0 = [
	[
		[ True, False, True ],
		[ False, True, False ],
		[ True, False, True ],
	],
	4,
]

t1 = [
	[
		[ True, True, False, True, False, True, False, True, True, False ],
		[ True, True, False, False, False, False, True, True, True, False ],
		[ True, True, False, False, False, False, False, False, False, True ],
		[ False, True, False, False, False, False, True, True, False, False ],
	],
	11567,
]

t2 = [
	[
		[ True, False, True, False, False, True, True, True ],
		[ True, False, True, False, False, False, True, False ],
		[ True, True, True, False, False, False, True, False ],
		[ True, False, True, False, False, False, True, False ],
		[ True, False, True, False, False, True, True, True ],
	],
	254,
]

t3 = [
	[
		[
			True
			for _ in range( 50 )
		]
		for _ in range( 9 )
	],
	100663356,
]

t4 = [
	[
		[
			False
			for _ in range( 50 )
		]
		for _ in range( 9 )
	],
	342015522530891220930318205106520120995761507496882358868830383880718255659276117597645436150624945088901216664965365050,
]

t5 = [
	[
		[
			choice( [ True, False ] )
			for _ in range( 50 )
		]
		for _ in range( 9 )
	],
	-1,
]



for index, test in enumerate( [ t0, t1, t2, t3, t4, t5 ] ):
	results = Grid.fromLists( test[0] ).solve()
	
	print( f'Test {index}: ', end = '' )
	if results == test[1] or test[1] == -1:
		print( f'success!' )
	else:
		print( f'faileds! Returned {results} instead of {test[1]}.' )



# import timeit
# time = timeit.timeit( lambda: Grid.fromLists( t4[0] ).solve(), number = 1 ) / 1
# print( f' Result: {time:,.3f}s' )



# import sys
# import trace
# tracer = trace.Trace(
#	ignoredirs = [ sys.prefix, sys.exec_prefix ],
#	trace = 0,
#	count = 1,
# )
# tracer.run( 'Grid.fromLists( t4[0] ).solve()' )
# r = tracer.results()
# r.write_results( show_missing = True, coverdir = '.' )



# By-Column results:
# 50x9 (All True): 78s
# 50x9 (All False): 243s
# 50x9 (Random): 108s

# By-Cell results (Loop slice):
# 50x9 (All True): 0.057s
# 50x9 (All False): 91s
# 50x9 (Random): 1.391s

# Loop slice:
# First column: 1.579s
# Column solutions: 58.317s
# Merge solutions.: 39.796s

# Bit slice:
# First column: 1.282s
# Column solutions: 60.045s
# Merge solutions: 9.045s

# Column solutions:
# First row.: 0.002s
# Single cell solutions.: 0.002s
# Append cell solutions.: 4.601s
# Merge cell solutions.: 54.517s

# Column solutions (last merge out of loop):
# First row.: 0.002s
# Single cell solutions.: 0.002s
# Append cell solutions.: 4.579s
# Merge cell solutions.: 31.876s

# Column solutions (merge on append):
# First row.: 0.003s
# Single cell solutions.: 0.003s
# Append cell solutions.: 8.396s