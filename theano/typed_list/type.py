from theano import gof


class TypedListType(gof.Type):

    def __init__(self, ttype, depth=0):
        """
        :Parameters:
            -'ttype' : Type of theano variable this list
            will contains, can be another list.
            -'depth' : Optionnal parameters, any value
            above 0 will create a nested list of this
            depth. (0-based)
        """
        if depth < 0:
            raise ValueError('Please specify a depth superior or'
                            'equal to 0')
        if not isinstance(ttype, gof.Type):
            raise TypeError('Expected a Theano Type')

        if depth == 0:
            self.ttype = ttype
        else:
            self.ttype = TypedListType(ttype, depth - 1)

    def filter(self, x, strict=False, allow_downcast=None):
        """
        :Parameters:
            -'x' : value to filter
            -'strict' : if true, only native python list will be accepted
            -'allow_downcast' : does not have any utility at the moment
        """
        if strict:
            if not isinstance(x, list):
                raise TypeError('Expected a python list')
        else:
            x = [self.ttype.filter(y) for y in x]

            if all(self.ttype.is_valid_value(y) for y in x):
                return x

            else:
                raise TypeError('Expected all elements to'
                                ' be %s' % str(self.ttype))

    def __eq__(self, other):
        """
        two list are equals if they contains the same type.
        """

        return  type(self) == type(other) and self.ttype == other.ttype

    def __hash__(self):
        return gof.hashtype(self) ^ hash(self.ttype)

    def __str__(self):
        return 'TypedList <' + str(self.ttype) + '>'

    def get_depth(self):
        """
        utilitary function to get the 0 based
        level of the list
        """
        if isinstance(self.ttype, TypedListType):
            return self.ttype.get_depth() + 1
        else:
            return 0
