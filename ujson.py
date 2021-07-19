
_NULL = object()

class SOW:
    """Hacky Simple Object Wrapper to simplify navigation of complex JSON objects.
    
    >>> s = SOW({'nested': {'stuff': ['a', 'b']}})
    >>> s.nested.stuff._0  # instead of s['nested']['stuff'][0]
    'a'
    """

    def __init__(self, obj):
        """params:
            obj - python object (nested dict/list/basic type)
                  as e.g. received from json.loads('..').
        """
        self.obj = obj

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        o = _NULL
        if type(self.obj) is dict:  # dict?
            if name in self.obj:
                o = self.obj[name]
        elif type(self.obj) is list:  # ..list?
            idx = name.lstrip('_')
            o = self.obj[int(idx)]
        
        if o is _NULL:
            raise(AttributeError(name))
        if type(o) in (type(None), bool, int, float, str):
            return o  # return basic type directly
        return SOW(o)  # but wrap nested dict/list

    def __repr__(self):
        return 'SOW( %s )' % (self.obj,)


if __name__ == '__main__':
    from doctest import testmod
    testmod()

