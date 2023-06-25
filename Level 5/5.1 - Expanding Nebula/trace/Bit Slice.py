from typing import Self
from collections import Counter, defaultdict
from itertools import chain



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
	
	
	def columnSolutions( self, x: int ) -> list[Self]:
		column = self.sliceVertical( x )
		cells = [ column.sliceHorizontal( y ) for y in range( self.height ) ]
		
		solutionsByKey = defaultdict( list )
		for cellSolution in cells[0].singleCellSolutions():
			bottom = cellSolution.sliceHorizontal( 1 )
			solutionsByKey[bottom].append( [ cellSolution ] )
		
		for cell in cells[1:]:
			nextSolutionsByKey = defaultdict( list )
			
			for cellSolution in cell.singleCellSolutions():
				top = cellSolution.sliceHorizontal( 0 )
				bottom = cellSolution.sliceHorizontal( 1 )
				
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



import sys
import trace
tracer = trace.Trace(
	ignoredirs = [ sys.prefix, sys.exec_prefix ],
	trace = 0,
	count = 1,
)
tracer.run( 'Grid.fromLists( t4[0] ).solve()' )
r = tracer.results()
r.write_results( show_missing = True, coverdir = '.' )