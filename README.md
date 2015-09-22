# Thunctor

Safe recursion with monads.

```python
@unroll
def fact(me, n):
    return (Thunk(1)
        if not n
        else Thunk(n-1).bind(me).map(lambda x: x * n))
```

```sh
$ pip install thunctor
```

## The Thunk Monad

The thunk monad allows for a lazy value to be constructed whose manipulations
will be delayed. These values can then be unrolled without exhausting the
callstack.

- `Thunk : a → Thunk a`
- `Thunk#bind : Thunk a → (a → Thunk b) → Thunk b`
- `Thunk#map : Thunk a → (a → b) → Thunk b`

A thunk returning function can be transformed to a normal function using
`unroll`.

- `unroll : ((*x, **y) → Thunk a) → (*x, **y) → a`

