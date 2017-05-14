# current version of pattern match only supports the match
# can be done with == operator. For example pattern matching
# works fine with int, string, char but not list since two
# lists can't be compared by == operator

# match int, return argument + 2
def test1( a ):
    res = pmatch ( a ):
        with 1:
            3
        with 2:
            4
        with 3:
            5
        with 4:
            6
    return res

# match string
def test2( a ):
    res = pmatch ( a ):
        with 'string1':
            'string1 matched'
        with 'string2':
            'string2 matched'
        with 'string with space':
            'with space matched'
    return res


# match expr
def test3():
    res = pmatch( 3 + 5 ):
       with 8:
           'right answer'
    return res

# match list ( not supported for current version )
def test4( a ):
    res = pmatch ( a ):
        with [ 1, 2, 3 ]:
            'int 1 2 3'
        with [ '1', '2', '3' ]:
            'char 1 2 3'
        with [ True, False, True ]:
            'bool t f t'
    return res

# match bool
def test5( a ):
    res = pmatch ( a ):
        with True:
            'true'
        with False:
            'false'
    return res


def main():
    assert( test1( 1 ) == 3 )
    assert( test1( 3 ) == 5 )
    assert( test2( 'string1' ) == 'string1 matched' )
    assert( test2( 'string with space' ) == 'with space matched' )
    assert( test3() == 'right answer' )
    assert( test4( [ 1, 2, 3 ] ) == 'int 1 2 3' )
    assert( test4( [ '1', '2', '3' ] ) == 'char 1 2 3' )
    assert( test5( True ) == 'true' )
    assert( test5( False ) == 'false' )
