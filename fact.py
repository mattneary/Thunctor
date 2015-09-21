from lib.thunctor import Thunk, think

@think
def fact(me, n):
    if not n:
        return Thunk(1)
    else:
        return Thunk(n-1).bind(me).map(lambda x: x * n)

print(fact(6))

