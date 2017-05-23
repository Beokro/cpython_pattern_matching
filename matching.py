# important variable used in mat and case
to_match_object = None
match_success = True

# class for match
class AllObject():
    # a place holder, AllObject match everything
    def __init__( self ):
        pass

class MatchPattern():
    # base class, all class inherit it need to
    # implement match( pattern, to_match ) method
    pass

class obj():
    # place holder for a list, used to match a class
    # for example obj( Person, 'ID', name = 'me' ) means the object
    # should have variable ID and name, name must be 'me'
    # to match it, object must be a instance of Person
    def __init__( self, *args, **kwargs ):
        self.args = args
        self.kwargs = kwargs

class com():
    # in order to match com( combination ), to_match must match all of the pattern
    # included in sum
    def __init__( self, *args ):
        self.args = args

class UnmatchError( Exception ):
    pass

class match_wrap:
    # create a simple context managers for with statement
    # save the match_target of outer scope if it already exist
    def __enter__( self ):
        global match_success
        match_success = False
        return self

    def __exit__( self, *args ):
        global to_match_object
        global match_success
        # restore the previous match name on exist
        if self.previous_match_target != None:
            to_match_object = self.previous_match_target
        else:
            to_match_object = None
        if not match_success:
            match_success = True
            raise UnmatchError
        match_success = True

    def __init__( self, match_target ):
        global to_match_object
        if to_match_object != None:
            self.previous_match_target = caller.f_locals[ to_match_name ]
        else:
            self.previous_match_target = None
        to_match_object = match_target

# _ can be used to match all objects
_ = AllObject()


def mat( match_target ):
    # just a wraper for match target
    return match_wrap( match_target )

def case( pattern ):
    global match_success
    # if previous match already success, quit
    if match_success or not match( pattern, to_match_object ):
        return False
    else:
        match_success = True
        return True

def match( pattern, to_match ):
    typeObject = type( int )
    if isinstance( pattern, AllObject ):
        return True

    if type( pattern ) == typeObject and type( to_match ) != typeObject:
        matching = TypeToValue( pattern )
    elif type( to_match ) == typeObject and type( pattern ) != typeObject:
        matching = TypeToValue( to_match )
        to_match = pattern
    elif type( pattern ) == list or type( pattern ) == tuple :
        matching = ListOrTuple( pattern )
    elif type( pattern ) == dict:
        matching = DictToDict( pattern )
    elif type( pattern ) == type( match ):
        matching = FunToValue( pattern )
    elif isinstance( pattern, obj ):
        matching = ClassToInstance( pattern )
    elif isinstance( pattern, com ):
        matching = CombinationToInstance( pattern )
    else:
        # take care of basetype and value
        matching = ValueToValue( pattern )

    return matching.match( to_match )


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

class DictToDict( MatchPattern ):
    # match a dict to another dict
    # to_match should have all the map of pattern
    def __init__( self, pattern ):
        self.pattern = pattern

    def match( self, to_match ):
        if type( to_match ) != dict:
            return False
        for key, value in self.pattern.iteritems():
            if not key in to_match:
                return False
            if not match( value, to_match[ key ] ):
                return False
        return True

class FunToValue( MatchPattern ):
    # pattern is a function, match if function return True
    def __init__( self, pattern ):
        self.pattern = pattern

    def match( self, to_match ):
        return self.pattern( to_match )


class ClassToInstance( MatchPattern ):
    def __init__( self, pattern ):
        assert( isinstance( pattern, obj ) )
        self.pattern = pattern.args
        self.withValuePattern = pattern.kwargs

    def match( self, to_match ):
        if len( self.pattern ) == 0:
            return True
        checkIndex = 0
        # if object has a type limit, check if to_match is the
        # instance of that certain type
        if type( self.pattern[ 0 ] ) == type( MatchPattern ):
            checkIndex = 1
            if not isinstance( to_match, self.pattern[ 0 ] ):
                return False
        for i in range( checkIndex, len( self.pattern ) ):
            if not hasattr( to_match, self.pattern[ i ] ):
                return False

        for attr, value in self.withValuePattern.iteritems():
            if not hasattr( to_match, attr ):
                return False
            if not match( value, getattr( to_match, attr ) ):
                return False
        return True

class CombinationToInstance( MatchPattern ):
    def __init__( self, pattern ):
        assert( isinstance( pattern, com ) )
        self.patterns = pattern.args

    def match( self, to_match ):
        for pattern in self.patterns:
            if not match( pattern, to_match ):
                return False
        return True
