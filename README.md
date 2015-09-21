# thunctor

Avoid `maximum recursion depth exceeded` errors in Python with thunks.

```python
@think
def fact(me, n):
    return (Thunk.val(1)
        if not n
        else Thunk(me, n-1).map(lambda x: x * n))
```

