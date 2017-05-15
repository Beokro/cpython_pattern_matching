from matching import match
# test on base type int, str, tuple, list, bool


# base value to base value test
assert( match( 1, 1 ) )
assert( match( 'haha', 'haha' ) )
assert( match( 1 + 2, 3 ) )
assert( match( True, True ) )
assert( match( ( 1, 2 ), ( 1, 2 ) ) )
assert( match( 1, 'haha' ) == False )
assert( match( 'lala', 'haha' ) == False )
assert( match( 1 + 2, 5 ) == False )
assert( match( True, False ) == False )
assert( match( ( 1, 2 ), ( 1, 4 ) ) == False )

# one is type, another is value
assert( match( int, 1 ) )
assert( match( str, 'haha' ) )
assert( match( str, 'haha' + 'lala' ) )
assert( match( bool, True ) )
assert( match( bool, False ) )
assert( match( list, [ 1, 2, 3, 4 ] ) )
assert( match( list, [ 'haha', 1, 2, 3, 'lala' ] ) )
assert( match( tuple, ( 1, 2 ) ) )
assert( match( tuple, ( 'haha', 'lala' ) ) )

assert( match( int, 'haha' ) == False )
assert( match( str, 123 ) == False )
assert( match( int, [ 1, 2, 3 ] ) == False )
assert( match( str, ( 1, 2 ) ) == False )
assert( match( bool, 123 ) == False )
assert( match( bool, ( 1, 2 ) ) == False )
assert( match( tuple, 123 ) == False )
assert( match( list, ( 1, 2 ) ) == False )
assert( match( tuple, [ 1, 2, 3, 4 ] ) == False ) 

print 'test passed'
