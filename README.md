# cpython_pattern_matching

Tried to add a new keyword to cpython lanuage but that didn't work out. Now try to write a library for pattern matching instead of changing the lanuage itslef

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
