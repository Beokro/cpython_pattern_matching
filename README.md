# cpython_pattern_matching
This project is intended to build a pattern matching for python.

## Basic Syntax
  <pre>
  count = 0
  with mat( 5 ):
    if case( int ):
      count += 1
    if case( 5 ):
      count += 2
    if case( list ):
      count += 4
      
  assert( count == 1 )
  </pre>
* pattern matching will throw a exception if no pattern matched for the target
* pattern matching will stop at first matched and exit the match
* pattern matching does not support multi threads but recurssion is fine

## Match And Assign
  <pre>
  class Con( object ):
    def __init__( self, xx, xxs ):
        # x is a number and xs is a Con
        self.x = xx
        self.xs = xxs

  def sum( con ):
    with mat( con ):
        if case( Con( _x, None ) ):
            return _x[ 0 ]
        if case( Con( _x, _xs ) ):
            return _x[ 0 ] + sum( _xs[ 0 ] )
        if case( _ ):
            print 'does not match with anything'
            return 0
            
  assert( sum( Con( 1, Con( 2, Con( 3, None ) ) ) ) == 6 )
  </pre>

* If you want to use Match and Assign, you have to use one of the pre defined var name including _x, _xs, _y, _z, _a, _b, _c, _d, _e, _f, _g
* The class you trying to match must inherit from object class
* Instead of use the variable directly, you have to add [ 0 ] after the variable to access the object/val you want

## back end match function
* match actual value
  <pre>
  match( 1, 1 ) = True
  match( 'haha', 'hah' ) = False
  </pre>
* match basic type to value. <br />
  <pre>
  match( 1, int ) = True
  match( str, 'haha' ) = True
  </pre>
* match self define type to value<br />
  <pre>
  class Person:
    def __init__( self )
      self.name = ' '
      self.ID = 0
  class Student( Person ):
    def __init__:
      Person.__init__()
      self.studentID = 1   
      
  p1 = Person()
  s1 = Student()
  match( obj( Person ), p1 ) = True
  match( obj( Student ), p1 ) = False
  match( obj( Person ), s1 ) = True
  match( obj( Person, studentID = 1 ), p1 ) = False
  </pre>
* match list
  <pre>
  match( [ 1, int, 'haha' ], [ int, 3, str ] ) = True
  match( [ str, str, 1 ], [ 'haha', str, 2 ] ) = False
  </pre>
* match tuple
  <pre>
  match( ( 1, 2 ), ( int, 2 ) ) = True
  match( ( 'haha', 'hahaha' ), ( 'hahaha', str ) ) = False
  </pre>
* match dictionary, partiality is accepted
  <pre>
  match( [ dict( [ ( a, 0 ), ( b, 1 ) ] ) ], { 'a' : 0, 'b' : 1, 'c' : 2 } ) = True
  match( [ dict( [ ( a, 0 ), ( b, 1 ), ( c, 2 ) ] ) ], { 'a' : 0, 'b' : 1} ]) = False
  </pre>
* match function
  <pre>
  def test1( val ):
    return val > 3
    
  match( test1, 5 ) = True
  match( lambda x: x > 100, 101 ) = True
  match( test1, 2 ) = False
  </pre>
* match combination of conditions
  <pre>
  match( com( int, lambda x: x > 100 ), 101 ) = True
  match( com( [ 1, 2, 3 ], lambda x: len( x ) == 5 ), [ 1, 2, 3 ] ) = False
  </pre>
* match _ ( always True )
  <pre>
  match( _, 'haha' ) = True
  match( _, 1234 ) = True
  match( _, [ 1234, 'haha' ] ) = True
  </pre>
