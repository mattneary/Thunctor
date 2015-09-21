# thunctor

Safe recursion with monads.

```python
@think
def fact(me, n):
    return (Thunk(1)
        if not n
        else Thunk(n-1).bind(me).map(lambda x: x * n))
```

