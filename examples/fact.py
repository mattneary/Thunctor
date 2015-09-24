from thunctor import Thunk, unroll

@unroll
def fact(me, n):
    if not n:
        return Thunk(1)
    else:
        return me(n-1).map(lambda x: x * n)

print(fact(6))

