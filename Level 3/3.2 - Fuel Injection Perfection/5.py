def solution( pellets ):
	pellets = int( pellets )
	
	operations = 0
	while pellets > 1:
		if pellets % 2 == 0:
			pellets //= 2
		elif pellets % 0b100 == 0b11 and pellets > 0b11:
			# Subtracting one from an odd number will always unset exactly one bit, while adding one will always set one
			# bit and unset one or more. Therefore we always choose the addition if we can be sure that it will unset
			# at least two bits, unless the one bit that will be set results in one extra division, in that case the
			# addition must unset at least three bits.
			pellets += 1
		else:
			pellets -= 1
		
		operations += 1
	
	return operations



print( solution( '1' ) == 0 )
print( solution( '2' ) == 1 )
print( solution( '3' ) == 2 )
print( solution( '4' ) == 2 )
print( solution( '5' ) == 3 )
print( solution( '6' ) == 3 )
print( solution( '7' ) == 4 )
print( solution( '8' ) == 3 )
print( solution( '9' ) == 4 )
print( solution( '10' ) == 4 )
print( solution( '11' ) == 5 )
print( solution( '12' ) == 4 )
print( solution( '13' ) == 5 )
print( solution( '14' ) == 5 )
print( solution( '15' ) == 5 )
print( solution( '16' ) == 4 )
print( solution( '17' ) == 5 )
print( solution( '18' ) == 5 )
print( solution( '23' ) == 6 )
print( solution( '39' ) == 7 )
print( solution( '59' ) == 8 )
print( solution( '191' ) == 9 )
print( solution( '223' ) == 10 )
print( solution( '255' ) == 9 )
print( solution( '614' ) == 13 )
print( solution( '1024' ) == 10 )



# 0							0000	X	0
# 1		0001	X	0
# 2							0010	/	1
# 3		0011	-	2
# 4							0100	/	2
# 5		0101	-	3
# 6							0110	/	3
# 7		0111	-+	4
# 8							1000	/	3
# 9		1001	-	4
# 10						1010	/	4
# 11	1011	-+	5
# 12						1100	/	4
# 13	1101	-	5
# 14						1110	/	5
# 15	1111	+	5
# 16						10000	/	4
# 17   10001	-	5
# 18   						10010	/	5

# 7
#  111 +
# 1000 / 3
#    1 = 4

# 7
#  111 -
#  110 /
#   11 -
#   10 /
#      1 = 4

# 15
#   1111 +
# 1 0000 / 4
#      1 = 5

# 23
# 1 0111 +
# 1 1000 / 3
#     11 -
#     10 /
#      1 = 6

# 39
# 10 0111 +
# 10 1000 / 3
#     101 -
#     100 / 2
#       1 = 7

# 59
# 11 1011 +
# 11 1100 / 2
#    1111 +
#  1 0000 / 4
#       1 = 8

# 191
# 1011 1111	+
# 1100 0000	/ 6
#        11 -
#        10 /
#         1 = 9

# 223
# 1101 1111	+
# 1110 0000 / 5	
#       111 +
#      1000 / 3
#         1 = 10

# 223
# 1101 1111	+
# 1110 0000 / 5	
#       111 -
#       110 /
#        11 -
#        10 /
#         1 = 10

# 255
#   1111 1111	+
# 1 0000 0000	/ 8
#           1	= 9