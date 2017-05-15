from matching import match
# test on base type int, str, tuple, list, bool


# base value to base value test
assert( match( 1, 1 ) )
assert( match( 'haha', 'haha' ) )
assert( match( 1 + 2, 3 ) )
assert( match( True, True ) )
assert( match( ( 1, 2 ), ( 1, 2 ) ) )

assert( not match( 1, 'haha' ) )
assert( not match( 'lala', 'haha' ) )
assert( not match( 1 + 2, 5 ) )
assert( not match( True, False ) )
assert( not match( ( 1, 2 ), ( 1, 4 ) ) )

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
assert( match( 1, int ) )
assert( match( 'haha', str ) )
assert( match( 'haha' + 'lala', str ) )
assert( match( True, bool ) )
assert( match( False, bool ) )

assert( not match( int, 'haha' ) )
assert( not match( str, 123 ) )
assert( not match( int, [ 1, 2, 3 ] ) )
assert( not match( str, ( 1, 2 ) ) )
assert( not match( bool, 123 ) )
assert( not match( bool, ( 1, 2 ) ) )
assert( not match( tuple, 123 ) )
assert( not match( list, ( 1, 2 ) ) )
assert( not match( tuple, [ 1, 2, 3, 4 ] ) )
assert( not match( 'haha', int ) )
assert( not match( 123, str ) )
assert( not match( [ 1, 2, 3 ], int ) )
assert( not match( ( 1, 2 ), str ) )
assert( not match( 123, bool ) )


# list to list
assert( match( [ 1, 2, 3 ], [ 1, 2, 3 ] ) )
assert( match( [ int, int, str ], [ 1, 123, 'haha' ]  ) )
assert( match( [ int, 1, str ], [ 123, 1, 'asdsa' ] ) )
assert( match( [ str, 'haha', 'lala' ], [ ' ', 'haha', 'lala' ] ) )
assert( match( [ [ str, str ], str ], [ [ 'haha', 'lol' ], 'olo' ] ) )
assert( match( [ bool, [ int, bool ], bool ], [ True, [ 1, False ], True ] ) )
assert( match( [ [ [ [ str ]]]], [ [ [ [ ' ' ]]]] )  )
assert( match( [], [] ) )

assert( not match( [ 1, 2, 3 ], [ 1, 2 ] ) )
assert( not match( [ str, int, int ], [ 3, ' ', 4 ] ) )
assert( not match( [ int, int, int, str ], [ 1, 1, 1, 1 ] ) )
assert( not match( [ bool, int, str, int ], [ True, 3, ' ', [] ] ) )
assert( not match( [ [ str, str ] ], [ [ 1, ' ' ] ] ) )
assert( not match( [ [ str, bool ], str ], [ [ ' ', True ], 1 ] ) )
assert( not match( [ [] ], [  ] ) )

class Person:
    def __init__( self ):
        self.ID = 0
        self.name = ' '

student = Person()
print type( student )

print 'test passed'
