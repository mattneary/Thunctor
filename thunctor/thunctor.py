class Thunk(object):
    def __init__(self, val):
        self.val = val
        self.mapper = []
    def bind(self, fn):
        return self.bind_many([fn])
    def bind_many(self, fns):
        self.mapper = fns + self.mapper
        return self
    def map(self, fn):
        return self.bind(lambda x: Thunk(fn(x)))
    def unroll(self):
        '''Apply one mapping and bind the rest to the resulting thunk.'''
        if not self.mapper:
            return self.val
        else:
            return self.mapper[-1](self.val).bind_many(self.mapper[:-1])

def unroll(fn):
    def partial(*args, **kwargs):
        return fn(partial, *args, **kwargs)
    def wrapped(*args, **kwargs):
        res = partial(*args, **kwargs)
        while isinstance(res, Thunk):
            res = res.unroll()
        return res
    return wrapped

