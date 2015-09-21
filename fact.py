from lib.thunctor import Thunk, think

@think
def count(me, n):
    if not n:
        return Thunk.val(0)
    else:
        return Thunk(me, n-1).map(lambda x: x + 1)

print(count(1000))

