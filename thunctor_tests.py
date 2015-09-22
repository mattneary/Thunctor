import unittest

from thunctor import Thunk, unroll


class ThunkTest(unittest.TestCase):
    def assertThunksEqual(self, a, b):
        thunk1 = unroll(lambda me: a)()
        thunk2 = unroll(lambda me: b)()
        self.assertEqual(thunk1, thunk2)

class TestMonadLaws(ThunkTest):
    def test_law1(self):
        add = lambda a: lambda b: Thunk(a + b)
        self.assertThunksEqual(Thunk(1).bind(add(1)), Thunk(2))
        self.assertThunksEqual(Thunk(3).bind(add(-1)), Thunk(2))

    def test_law2(self):
        ret = lambda a: Thunk(a)
        self.assertThunksEqual(Thunk(1).bind(ret), Thunk(1))
        self.assertThunksEqual(Thunk(5).bind(ret), Thunk(5))

    def test_law3(self):
        f = lambda a: Thunk(a + 2)
        g = lambda a: Thunk(a * 2)
        self.assertThunksEqual(Thunk(1).bind(f).bind(g), Thunk(1).bind(lambda x: f(x).bind(g)))
        self.assertThunksEqual(Thunk(3).bind(f).bind(g), Thunk(3).bind(lambda x: f(x).bind(g)))

class TestNesting(ThunkTest):
    def test_chained_maps(self):
        add = lambda a: lambda b: a + b
        self.assertThunksEqual(Thunk(1).map(add(1)), Thunk(2))
        self.assertThunksEqual(Thunk(1).map(add(1)).map(add(2)), Thunk(4))

    def test_map_in_bind(self):
        add = lambda a: lambda b: a + b
        addT = lambda a: lambda b: Thunk(a + b)
        self.assertThunksEqual(Thunk(1).bind(lambda x:
            addT(2)(x).map(add(1))), Thunk(4))
        self.assertThunksEqual(Thunk(1).bind(lambda x:
            addT(2)(x).map(lambda _: x)), Thunk(1))

    def test_bind_in_bind(self):
        addT = lambda a: lambda b: Thunk(a + b)
        self.assertThunksEqual(Thunk(1).bind(lambda x:
            addT(2)(x).bind(addT(1))), Thunk(4))

    def test_multi_bind(self):
        addT = lambda a: lambda b: Thunk(a + b)
        self.assertThunksEqual(Thunk(1).bind(addT(2)).bind(addT(1)), Thunk(4))

    def test_mutating_bind(self):
        addT = lambda a: lambda b: Thunk(a + b)
        t = Thunk(1)
        t.bind(addT(2))
        t.bind(addT(1))
        self.assertThunksEqual(t, Thunk(4))

    def test_mutating_bind_maps(self):
        t = Thunk(1)
        t.bind(lambda x: Thunk(1).map(lambda _: x))
        t.bind(lambda x: Thunk(1).map(lambda _: x))
        self.assertThunksEqual(t, Thunk(1))

        t = Thunk(1)
        ts = [Thunk(1), Thunk(1)]
        t.bind(lambda x: ts[0].map(lambda _: x))
        t.bind(lambda x: ts[1].map(lambda _: x))
        self.assertThunksEqual(t, Thunk(1))

        t = Thunk(1)
        ts = {'a': Thunk(1), 'b': Thunk(1)}
        t.bind(lambda x: ts['a'].map(lambda _: x + 1))
        t.bind(lambda x: ts['b'].map(lambda _: x + 1))
        self.assertThunksEqual(t, Thunk(3))

        t = Thunk({})
        ts = {'a': Thunk(1), 'b': Thunk(1)}
        t.bind(lambda x: ts['a'].map(lambda v: dict(x, **{'a': v})))
        t.bind(lambda x: ts['b'].map(lambda v: dict(x, **{'b': v})))
        self.assertThunksEqual(t, Thunk({'a': 1, 'b': 1}))

        t = Thunk({})
        ts = {'a': Thunk(1), 'b': Thunk(1)}
        k = 'a'
        t.bind(lambda x: ts[k].map(lambda v: dict(x, **{k: v})))
        k2 = 'b'
        t.bind(lambda x: ts[k2].map(lambda v: dict(x, **{k2: v})))
        self.assertThunksEqual(t, Thunk({'a': 1, 'b': 1}))

        t = Thunk({})
        ts = {'a': Thunk(1), 'b': Thunk(1)}
        def apply(t, k, v):
            t.bind(lambda x: ts[k].map(lambda v: dict(x, **{k: v})))
        for k, v in ts.iteritems():
            apply(t, k, v)
        self.assertThunksEqual(t, Thunk({'a': 1, 'b': 1}))

    def test_mutating_bind_and_map(self):
        add = lambda a: lambda b: a + b
        addT = lambda a: lambda b: Thunk(a + b)
        t = Thunk(1)
        t.bind(addT(2))
        t.map(add(1))
        self.assertThunksEqual(t, Thunk(4))

if __name__ == '__main__':
    unittest.main()

