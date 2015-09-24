from thunctor import Thunk, unroll

@unroll
def count(me, n):
    if not n:
        return Thunk(0)
    else:
        return me(n-1).map(lambda x: x + 1)

print(count(1000))

