from lib.thunctor import Thunk, think

@think
def count(me, n):
    if not n:
        return Thunk(0)
    else:
        return Thunk(n-1).bind(me).map(lambda x: x + 1)

print(count(1000))

