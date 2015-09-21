class Thunk(object):
    IS_THUNK = True
    def _compose(self, f, g):
        def h(*args, **kwargs):
            return f(g(*args, **kwargs))
        return h
    def __init__(self, val):
        self.val = val
        self.mapper = []
    def bind(self, fn):
        return self.bind_many([fn])
    def bind_many(self, fns):
        self.mapper = fns + self.mapper
        return self
    def unroll(self):
        if not self.mapper:
            return self.val
        else:
            return self.mapper[-1](self.val).bind_many(self.mapper[:-1])
    def map(self, fn):
        return self.bind(lambda x: Thunk(fn(x)))

def think(fn):
    def partial(*args, **kwargs):
        return fn(partial, *args, **kwargs)
    def wrapped(*args, **kwargs):
        res = partial(*args, **kwargs)
        while getattr(res, 'IS_THUNK', False):
            res = res.unroll()
        return res
    return wrapped

