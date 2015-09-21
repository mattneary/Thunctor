# thunctor

Avoid `maximum recursion depth exceeded` errors in Python with thunks.

```python
@think
def fact(me, n):
    return (Thunk(1)
        if not n
        else Thunk(n-1).bind(me).map(lambda x: x * n))
```

