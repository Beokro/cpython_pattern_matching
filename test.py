from matching import match, obj, _, com, mat, case, UnmatchError, _x, _xs
import matching
import inspect
import sys
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

# tuple to tuple
assert( match( ( 1, 2, 3 ), ( 1, 2, 3 ) ) )
assert( match( ( int, int, str ), ( 1, 123, 'haha' )  ) )
assert( match( ( int, 1, str ), ( 123, 1, 'asdsa' ) ) )
assert( match( ( str, 'haha', 'lala' ), ( ' ', 'haha', 'lala' ) ) )
assert( match( ( ( str, str ), str ), ( ( 'haha', 'lol' ), 'olo' ) ) )
assert( match( ( bool, ( int, bool ), bool ), ( True, ( 1, False ), True ) ) )
assert( match( ( ( ( ( str )))), ( ( ( ( ' ' )))) )  )
assert( match( (), () ) )

assert( not match( ( 1, 2, 3 ), ( 1, 2 ) ) )
assert( not match( ( str, int, int ), ( 3, ' ', 4 ) ) )
assert( not match( ( int, int, int, str ), ( 1, 1, 1, 1 ) ) )
assert( not match( ( bool, int, str, int ), ( True, 3, ' ', () ) ) )
assert( not match( ( ( str, str ) ), ( ( 1, ' ' ) ) ) )
assert( not match( ( ( str, bool ), str ), ( ( ' ', True ), 1 ) ) )
assert( not match( ( [] ), ()  ) )


# dict to dict
assert( match( { 'a' : 1, 'b' : 2 }, { 'a' : 1, 'b' : 2 } ) )
assert( match( { 'a' : 1, 'b' : 2 }, { 'a' : 1, 'b' : 2, 'c': 3 } ) )
assert( match( {}, { 'a' : 1 } ) )
assert( match( { 'lala' : 'haha' }, { 'lala' : 'haha' } ) )
assert( match( { 1 : 2, 3 : 4 }, { 3 : 4, 1 : 2 } ) )
assert( match( { 1 : [ int, int ] }, { 1 : [ 2, 3 ] } ) )


assert( not match( { 'a' : 1, 'b' : 2, 'c' : 3 }, { 'a' : 1, 'b' : 2 } ) )
assert( not match( { 'a' : 2, 'b' : 2 }, { 'a' : 1, 'b' : 2, 'c' : 3 } ) )
assert( not match( { 1 : 2 }, {} ) )
assert( not match( { 11 : 2 }, { 1 : 2 } ) )
assert( not match( { 111 : [ int, int ] }, { 111 : [ 1, '1' ] } ) )
assert( not match( { 123 : int }, { 123 : [ 1 ] } ) )
assert( not match( { 'haha' : "lala" }, { 'lala' : 'haha' } ) )

# match a val using function
def test1( val ):
    return val > 3

def test2( val ):
    return len( val ) > 3

def test3( val ):
    return val == 'haha'

assert( match( test1, 5 ) )
assert( match( test1, 100 ) )
assert( match( test2, [ 1, 2, 3, 4 ] ) )
assert( match( test2, [ 'hha', 'lala', 'zaza',1234 ] ) )
assert( match( test3, 'haha' ) )
assert( match( lambda x: x > 100, 101  ) )

assert( not match( test1, 2 ) )
assert( not match( test1, -10000 ) )
assert( not match( test2, [] ) )
assert( not match( test2, [ 1, 'lala' ] ) )
assert( not match( test3, 'what is up' ) )
assert( not match( lambda x: x > 100, 99 ) )

# match a self define class
class Person:
    def __init__( self ):
        self.ID = 0
        self.name = ' '

class Student( Person ):
    def __init__( self ):
        Person.__init__( self )
        self.studentID = 1
        self.units = 0

class Police( Person ):
    def __init__( self ):
        Person.__init__( self )
        self.policeID = 2

person_a = Person()
student_a = Student()
student_a.studentID = 2
police_a = Police()

assert( match( obj( Person ), person_a ) )
assert( match( obj( Person ), student_a ) )
assert( match( obj( Student ), student_a ) )
assert( match( obj( Police ), police_a ) )
assert( match( obj( Person, 'policeID' ), police_a ) )
assert( match( obj( Person, 'studentID' ), student_a ) )
assert( match( obj( Person, studentID = 2 ), student_a ) )
assert( match( obj( Person, studentID = 2, units = 0 ), student_a ) )

assert( not match( obj( Student ), person_a ) )
assert( not match( obj( Student ), police_a ) )
assert( not match( obj( Police ), person_a ) )
assert( not match( obj( Person, 'studentID' ), person_a ) )
assert( not match( obj( Person, 'policeID' ), person_a ) )
assert( not match( obj( Person, studentID = 3 ), student_a ) )
assert( not match( obj( Person, studentID = 2, units = 5 ), student_a ) )


# match _, always true
assert( match( _, person_a ) )
assert( match( _, ( 1, 2, 3 ) ) )
assert( match( _, ( 1, 123, 'haha' )  ) )
assert( match( _, [ 123, 1, 'asdsa' ] ) )
assert( match( _, [ ' ', 'haha', 'lala' ] ) )

# match combination
assert( match( com( int, lambda x: x > 100 ), 101 ) )
assert( match( com( obj( Person, 'policeID' ), lambda x: x.ID == 0 ), police_a ) )
assert( match( com( { 'a' : 1, 'b' : 2 }, lambda x: x[ 'a' ] == 1 ), { 'a' : 1, 'b' : 2 } ) )
assert( match( com( 1, int ), 1 ) )
assert( match( com( [ 1, 2, 3 ], lambda x: len( x ) == 3 ), [ 1, 2, 3 ] ) )

assert( not match( com( int, lambda x: x < 100 ), 101 ) )
assert( not match( com( obj( Person, 'policeID' ), lambda x: x.ID == 3 ), police_a ) )
assert( not match( com( { 'a' : 1, 'b' : 2 }, lambda x: x[ 'a' ] == 5 ), { 'a' : 1, 'b' : 2 } ) )
assert( not match( com( 1, int ), '1' ) )
assert( not match( com( [ 1, 2, 3 ], lambda x: len( x ) == 5 ), [ 1, 2, 3 ] ) )


def match_number( num ):
    counter = 0
    with mat( num ):
        if case( int ):
            counter += 1
        if case( 5 ):
            counter += 2
        if case( 4 ):
            counter += 4
        if case( _ ):
            counter += 8
    return counter

def match_Person( p ):
    with mat( p ):
        if case( obj( Police ) ):
            return 'police'
        if case( obj( Student ) ):
            return 'student'
        if case( obj( Person ) ):
            return 'person'

assert( match_number( 5 ) == 1 )
assert( match_number( 'haha' ) == 8 )
assert( match_Person( person_a ) == 'person' )
assert( match_Person( student_a ) == 'student' )
assert( match_Person( police_a ) == 'police' )

# test ablt pattern_match will throw a exception if nothing match
unmatch = False
try:
    match_Person( 1 )
except UnmatchError as e:
    unmatch = True
assert( unmatch )


# test on recurssion
def match_recur( num ):
    with mat( num ):
        if case( 0 ):
            return 0
        if case( com( int, lambda x: x > 0 ) ):
            return num + match_recur( num - 1 )
        if case( _ ):
            print 'recurssion matched failed'

assert( match_recur( 4 ) == 10 )


# test on match class with undeclare variable
class Con( object ):
    def __init__( self, xx, xxs ):
        # x is a number and xs is a Con
        self.x = xx
        self.xs = xxs

def match_Con( con ):
    with mat( con ):
        if case( Con( _x, _xs ) ):
            return _x[0]
        if case( _ ):
            print '...'
            return None

def sum( con ):
    with mat( con ):
        if case( Con( _x, None ) ):
            return _x[ 0 ]
        if case( Con( _x, _xs ) ):
            return _x[ 0 ] + sum( _xs[ 0 ] )
        if case( _ ):
            print 'does not match with anything'
            return 0

assert( match_Con( Con( 100, 2 ) ) == 100 )
assert( sum( Con( 1, Con( 2, Con( 3, None ) ) ) ) == 6 )

print 'test passed'
