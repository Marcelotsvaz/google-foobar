# Python 2.7.13 =(



def versionStringToTuple( versionString ):
	parts = iter( map( int, versionString.split( '.' ) ) )
	
	major = next( parts )
	minor = next( parts, -1 )		# -1 if missing.
	revision = next( parts, -1 )	# -1 if missing.
	
	return major, minor, revision



def solution( versionStringList ):
	return sorted( versionStringList, key = versionStringToTuple )



print( solution( ['1.11', '2.0.0', '1.2', '2', '0.1', '1.2.1', '1.1.1', '2.0'] ) )
print( [ '0.1', '1.1.1', '1.2', '1.2.1', '1.11', '2', '2.0', '2.0.0' ] )

print( solution( ['1.11', '2.0.0', '1.2', '2', '0.1', '1.2.1', '1.1.1', '2.0'] ) == [ '0.1', '1.1.1', '1.2', '1.2.1', '1.11', '2', '2.0', '2.0.0' ] )
print( solution( ['1.1.2', '1.0', '1.3.3', '1.0.12', '1.0.2'] ) == [ '1.0', '1.0.2', '1.0.12', '1.1.2', '1.3.3' ] )