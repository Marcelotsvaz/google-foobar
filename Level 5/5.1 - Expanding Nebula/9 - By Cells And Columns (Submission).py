# 
# Marcelo Tellier Sartori Vaz
# 
# https://github.com/Marcelotsvaz



from collections import Counter, defaultdict
from itertools import chain



class Grid:
	def __init__( self, gridAsInt, width, height ):
		self.width = width
		self.height = height
		self.gridAsInt = gridAsInt
	
	
	def __eq__( self, value ):
		return self.width == value.width and self.height == value.height and self.gridAsInt == value.gridAsInt
	
	
	def __hash__( self ):
		return hash( self.gridAsInt )
	
	
	def __getitem__( self, key ):
		return bool( self.gridAsInt >> self.height * key[0] + key[1] & 1 )
	
	
	def __setitem__( self, key, value ):
		if value:
			self.gridAsInt |= 1 << self.height * key[0] + key[1]
		else:
			self.gridAsInt &= ~( 1 << self.height * key[0] + key[1] )
	
	
	@classmethod
	def fromLists( cls, gridAsLists ):
		'''
		Create Grid from a list of lists.
		'''
		
		width = len( gridAsLists[0] )
		height = len( gridAsLists )
		
		# Convert to integer representation.
		grid = cls( 0, width, height )
		for y in range( height ):
			for x in range( width ):
				grid[x, y] = gridAsLists[y][x]
		
		return grid
	
	
	def singleCellSolutions( self ):
		'''
		Return hard-coded solutions to a 1x1 grid.
		'''
		
		if self.gridAsInt == 0:
			solutions = [ 0, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15 ]
		else:
			solutions = [ 1, 2, 4, 8 ]
		
		return [ self.__class__( gridAsInt, 2, 2 ) for gridAsInt in solutions ]
	
	
	def sliceVertical( self, x ):
		'''
		Return a 1-wide vertical slice.
		'''
		
		bitMask = 2 ** self.height - 1
		offset = x * self.height
		
		gridAsInt = self.gridAsInt >> offset & bitMask
		
		return self.__class__( gridAsInt, 1, self.height )
	
	
	def sliceHorizontal( self, y ):
		'''
		Return a 1-wide horizontal slice.
		'''
		
		gridSlice = self.__class__( 0, self.width, 1 )
		
		for x in range( self.width ):
			gridSlice[x, 0] = self[x, y]
		
		return gridSlice
	
	
	def columnSolutions( self, x ):
		'''
		Return an iterator containing all solutions to a single column.
		'''
		
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
	
	
	def solution( self ):
		'''
		Combine column solutions into the final solution.
		
		O( width * 2^height )
		'''
		
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
		
		return sum( solutionCounter.values() )



def solution( grid ):
	
	return Grid.fromLists( grid ).solution()