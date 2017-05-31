import inspect
# important variable used in mat and case
to_match_object = None
match_success = True
_x = [ '_x_place_holder' ]
_xs = [ '_xs_place_holder' ]
_y = [ '_y_place_holder' ]
_z = [ '_z_place_holder' ]
_a = [ '_a_place_holder' ]
_b = [ '_b_place_holder' ]
_c = [ '_c_place_holder' ]
_d = [ '_d_place_holder' ]
_e = [ '_e_place_holder' ]
_f = [ '_f_place_holder' ]
_g = [ '_g_place_holder' ]

def resetAllGlobal():
    _x[ 0 ] = '_x_place_holder'
    _xs[ 0 ] = '_xs_place_holder'
    _y[ 0 ] = '_y_place_holder'
    _z[ 0 ] = '_z_place_holder'
    _a[ 0 ] = '_a_place_holder'
    _b[ 0 ] = '_b_place_holder'
    _c[ 0 ] = '_c_place_holder'
    _d[ 0 ] = '_d_place_holder'
    _e[ 0 ] = '_e_place_holder'
    _f[ 0 ] = '_f_place_holder'
    _g[ 0 ] = '_g_place_holder'

def isGlobal( val ):
    return val == _x or val == _xs or val == _y or val == _z or val == _a  or\
        val == _b or val == _c or val == _d or val == _e or val == _f or val == _g 

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
        global _x, _xs, _y, _z, _a, _b, _c, _d, _e, _f, _g
        # restore the previous match name on exist
        to_match_object = self.previous_match_target
        _x[ 0 ] = self._x
        _xs[ 0 ] = self._xs
        _y[ 0 ] = self._y
        _z[ 0 ] = self._z
        _a[ 0 ] = self._a
        _b[ 0 ] = self._b
        _c[ 0 ] = self._c
        _d[ 0 ] = self._d
        _e[ 0 ] = self._e
        _f[ 0 ] = self._f
        _g[ 0 ] = self._g
        if not match_success:
            match_success = True
            raise UnmatchError
        match_success = True

    def __init__( self, match_target ):
        global to_match_object
        global _x, _xs, _y, _z, _a, _b, _c, _d, _e, _f, _g
        self.previous_match_target = to_match_object
        self._x = _x[ 0 ]
        self._xs = _xs[ 0 ]
        self._y = _y[ 0 ]
        self._z = _z[ 0 ]
        self._a = _a[ 0 ]
        self._b = _b[ 0 ]
        self._c = _c[ 0 ]
        self._d = _d[ 0 ]
        self._e = _e[ 0 ]
        self._f = _f[ 0 ]
        self._g = _g[ 0 ]
        resetAllGlobal()
        to_match_object = match_target

# _ can be used to match all objects
_ = AllObject()


def mat( match_target ):
    # just a wraper for match target
    return match_wrap( match_target )

def case( pattern ):
    global match_success
    resetAllGlobal()
    # if previous match already success, quit
    if match_success or not match( pattern, to_match_object ):
        return False
    else:
        match_success = True
        return True

def cond( *args ):
    global match_success
    for arg in args:
        if not arg:
            match_success = False
            return False
    return True

def match( pattern, to_match ):
    typeObject = type( int )
    patternType = type( pattern )
    if isinstance( pattern, AllObject ):
        return True

    if isGlobal( pattern ):
        matching = GlobalToAll( pattern )
    elif patternType == typeObject and type( to_match ) != typeObject:
        matching = TypeToValue( pattern )
    elif type( to_match ) == typeObject and patternType != typeObject:
        matching = TypeToValue( to_match )
        to_match = pattern
    elif len( str( patternType ) ) > 6 and str( patternType )[ 1 : 6 ] == 'class':
        matching = instanceAsPattern( pattern )
    elif patternType == list or patternType == tuple :
        matching = ListOrTuple( pattern )
    elif patternType == dict:
        matching = DictToDict( pattern )
    elif patternType == type( match ):
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

def instanceHelper( pattern, key, to_match ):
    attr = getattr( pattern, key )
    newAttr = getattr( to_match, key )
    return replaceGlobal( attr, newAttr )

def replaceGlobal( attr, newAttr ):
    # if pattern's attr is one of the holder, replace it with real value
    # otherwise do a mtach
    if attr == [ '_x_place_holder' ]:
        _x[ 0 ] = newAttr
    elif attr == [ '_xs_place_holder' ]:
        _xs[ 0 ] = newAttr
    elif attr == [ '_y_place_holder' ]:
        _y[ 0 ] = newAttr
    elif attr == [ '_z_place_holder' ]:
        _z[ 0 ] = newAttr
    elif attr == [ '_a_place_holder' ]:
        _a[ 0 ] = newAttr
    elif attr == [ '_b_place_holder' ]:
        _b[ 0 ] = newAttr
    elif attr == [ '_c_place_holder' ]:
        _c[ 0 ] = newAttr
    elif attr == [ '_d_place_holder' ]:
        _d[ 0 ] = newAttr
    elif attr == [ '_e_place_holder' ]:
        _e[ 0 ] = newAttr
    elif attr == [ '_f_place_holder' ]:
        _f[ 0 ] = newAttr
    elif attr == [ '_g_place_holder' ]:
        _g[ 0 ] = newAttr
    else:
        return match( attr, newAttr )
    return True



class instanceAsPattern( MatchPattern ):
    def __init__( self, pattern ):
        self.pattern = pattern

    def match( self, to_match ):
        if not isinstance( to_match, type( self.pattern ) ):
            return False
        # use pattern to find out which variable is used
        attrs = self.pattern.__dict__.keys()
        for i in range ( 0, len( attrs ) ):
            if not instanceHelper( self.pattern, attrs[ i ], to_match ):
                return False
        return True

class GlobalToAll( MatchPattern ):
    def __init__( self, pattern ):
        self.pattern = pattern

    def match( self, to_match ):
        return replaceGlobal( self.pattern, to_match )
