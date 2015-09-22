import unittest

from thunctor import Thunk, unroll

class TestMonadLaws(unittest.TestCase):
    def assertThunksEqual(self, a, b):
        thunk1 = unroll(lambda me: a)()
        thunk2 = unroll(lambda me: b)()
        self.assertEqual(thunk1, thunk2)

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

if __name__ == '__main__':
    unittest.main()

