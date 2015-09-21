class Thunk(object):
    IS_THUNK = True
    def _compose(self, f, g):
        def h(*args, **kwargs):
            return f(g(*args, **kwargs))
        return h
    def _fmap(self, x, fns):
        if getattr(x, 'IS_THUNK', False):
            return x.map_many(fns)
        else:
            res = x
            for fn in reversed(fns):
                res = fn(res)
            return res
    def __init__(self, action, *args, **kwargs):
        self.action = action
        self.args = args;
        self.kwargs = kwargs
        self.mapper = []
    def unroll(self):
        return self._fmap(self.action(*self.args, **self.kwargs), self.mapper)
    def map(self, fn):
        return self.map_many([fn])
    def map_many(self, fns):
        self.mapper = fns + self.mapper
        return self
    @classmethod
    def val(cls, x):
        return cls(lambda x: x, x)

def think(fn):
    def partial(*args, **kwargs):
        return fn(partial, *args, **kwargs)
    def wrapped(*args, **kwargs):
        res = partial(*args, **kwargs)
        while getattr(res, 'IS_THUNK', False):
            res = res.unroll()
        return res
    return wrapped

