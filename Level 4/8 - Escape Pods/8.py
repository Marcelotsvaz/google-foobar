def simplify( graph, nodesToMerge ):
	'''
	Move all edges connected to nodes `nodesToMerge[1:]` to `nodesToMerge[0]`.
	'''
	
	for nodeToMerge in nodesToMerge[1:]:
		for node in range( len( graph ) ):
			graph[nodesToMerge[0]][node] += graph[nodeToMerge][node]
			graph[node][nodesToMerge[0]] += graph[node][nodeToMerge]
			graph[nodeToMerge][node] = 0
			graph[node][nodeToMerge] = 0



def findPath( graph, start, end, visitedNodes = None ):
	'''
	Find a path from `start` to `end` using depth-first search.
	'''
	
	if start == end:
		return [ end ]
	
	if visitedNodes is None:
		visitedNodes = set()
	
	visitedNodes.add( start )
	
	for node, weight in enumerate( graph[start] ):
		if weight > 0 and node not in visitedNodes:
			path = findPath( graph, node, end, visitedNodes )
			
			if path:
				return [ start ] + path
	
	return None



def solution( entrances, exits, paths ):
	'''
	Find the maximum flow from all `entrances` to all `exits`.
	
	1) Merge all entrances and all exists into single nodes.
	2) Find a path between the entrance and the exit.
	3) Calculate the maximum flow through that path.
	4) Subtract that value from all segments along the path to represent the remaining capacity.
	5) Form a reverse path with capacity equal of the forward flow to effectively allow rearranging the flow using just
	the same pathfinding algorithm.
	6) Repeat steps 2~5 until there's no valid path.
	'''
	
	simplify( paths, entrances )
	simplify( paths, exits )
	
	flow = 0
	while True:
		path = findPath( paths, entrances[0], exits[0] )
		
		if not path:
			break
		
		# Smallest edge.
		maxFlow = min( map( lambda segment: paths[segment[0]][segment[1]], zip( path, path[1:] ) ) )
		
		for segment in zip( path, path[1:] ):
			paths[segment[0]][segment[1]] -= maxFlow
			paths[segment[1]][segment[0]] += maxFlow
		
		flow += maxFlow
	
	return flow



t1 = [
	[ 0 ],
	[ 3 ],
	[
		[ 0, 7, 0, 0 ],
		[ 0, 0, 6, 0 ],
		[ 0, 0, 0, 8 ],
		[ 9, 0, 0, 0 ],
	],
	6
]

t2 =[
	[ 0, 1 ],
	[ 4, 5 ],
	[
		[ 0, 0, 4, 6, 0, 0 ],
		[ 0, 0, 5, 2, 0, 0 ],
		[ 0, 0, 0, 0, 4, 4 ],
		[ 0, 0, 0, 0, 6, 6 ],
		[ 0, 0, 0, 0, 0, 0 ],
		[ 0, 0, 0, 0, 0, 0 ],
	],
	16
]

# t2 coalesced.
t3 =[
	[ 0 ],
	[ 3 ],
	[
		[ 0, 9, 8, 0 ],
		[ 0, 0, 0, 8 ],
		[ 0, 0, 0, 12 ],
		[ 0, 0, 0, 0 ],
	],
	16
]

#
t4 =[
	[ 0 ],
	[ 6 ],
	[
		[ 0, 8, 8, 0, 0, 0, 0 ],
		[ 0, 0, 0, 6, 4, 0, 0 ],
		[ 0, 0, 0, 6, 0, 3, 0 ],
		[ 0, 0, 0, 0, 0, 0, 8 ],
		[ 0, 0, 0, 0, 0, 0, 3 ],
		[ 0, 0, 0, 0, 0, 0, 4 ],
		[ 0, 0, 0, 0, 0, 0, 0 ],
	],
	14
]

t5 = [
	[ 0 ],
	[ 3 ],
	[
		[ 0, 7, 0, 0 ],
		[ 0, 0, 6, 0 ],
		[ 0, 0, 0, 0 ],
		[ 9, 0, 0, 0 ],
	],
	0
]

t6 = [
	[ 0 ],
	[ 3 ],
	[
		[ 0, 8, 8, 0 ],
		[ 0, 0, 1, 8 ],
		[ 0, 0, 0, 8 ],
		[ 0, 0, 0, 0 ],
	],
	16
]


# for test in [ t6 ]:
for test in [ t1, t2, t3, t4, t5, t6 ]:
	print( solution( test[0], test[1], test[2] ), test[3] )


# def test():
# 	for test in [ t1, t2, t3, t4, t5 ]:
# 		solution( test[0], test[1], test[2] )

# import timeit
# time = timeit.timeit( test, number = 1000 ) / 1000 * 10**6
# print( f' Result: {time:,.3f}us' )