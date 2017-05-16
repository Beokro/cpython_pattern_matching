# cpython_pattern_matching

Tried to add a new keyword to cpython lanuage but that didn't work out. Now try to write a library for pattern matching instead of changing the lanuage itslef

## Implemenation Goal
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
      self.name = ' '
      self.ID = 0
      
  student = Person()
  match( student, Person ) = True
  </pre>
* match list
  <pre>
  match( [ 1, int, 'haha' ], [ int, 3, str ] ) = True
  match( [ str, str, 1 ], [ 'haha', str, 2 ] ) = False
  </pre>
* match parentheses
  <pre>
  match( ( 1, 2 ), ( int, 2 ) ) = True
  match( ( 'haha', 'hahaha' ), ( 'hahaha', str ) ) = False
  </pre>
* match dictionary, partiality is accepted
  <pre>
  match( [ dict( [ ( a, 0 ), ( b, 1 ) ] ) ], { 'a' : 0, 'b' : 1, 'c' : 2 } ) = True
  match( [ dict( [ ( a, 0 ), ( b, 1 ), ( c, 2 ) ] ) ], { 'a' : 0, 'b' : 1} ]) = False
  </pre>
