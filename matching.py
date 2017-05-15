def match( pattern, to_match ):
    typeObject = type( int )
    if type( pattern ) == typeObject and type( to_match ) != typeObject:
        matching = TypeToValue( pattern )
    elif type( to_match ) == typeObject and type( pattern ) != typeObject:
        matching = TypeToValue( to_match )
        to_match = pattern
    elif type( pattern ) == list or type( pattern ) == tuple :
        matching = ListOrTuple( pattern )
    else:
        # take care of basetype and value
        matching = ValueToValue( pattern )

    return matching.match( to_match )


class MatchPattern():
    # base class, all class inherit it need to
    # implement match( pattern, to_match ) method
    pass

class ValueToValue( MatchPattern ):
    # both pattern and to_match is value
    def __init__( self, pattern ):
        self.pattern = pattern
    def match( self, to_match ):
        return self.pattern == to_match

class TypeToValue( MatchPattern ):
    # pattern is a type, to_match is a value
    def __init__( self, pattern ):
        self.pattern = pattern
    def match( self, to_match ):
        return isinstance( to_match, self.pattern )

class ListOrTuple( MatchPattern ):
    # match a list to another list
    def __init__( self, pattern ):
        self.pattern = pattern
        assert( type( self.pattern ) == list or type( self.pattern ) == tuple )
    def match( self, to_match ):
        if ( type( to_match ) != list and type( to_match ) != tuple ) or\
           type( to_match ) != type( self.pattern ):
            return False
        if len( self.pattern ) != len( to_match ):
            return False
        for i in range ( len( self.pattern ) ):
            if not match( self.pattern[ i ], to_match[ i ] ):
                return False
        return True
