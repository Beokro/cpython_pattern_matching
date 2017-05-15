def match( pattern, to_match ):
    typeObject = type( int )
    if type( pattern ) == typeObject and type( to_match ) != typeObject:
        matching = TypeToValue( pattern )
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

