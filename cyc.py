from sympy import mod_inverse

class ModArith:
    def __init__(self, val, mod):
        if isinstance(val, ModArith):
            assert(mod == val.m)
            self.val = val.val
            self.m = mod
        else:
            self.val = val % mod
            self.m = mod

    def __add__(self, other):
        assert(isinstance(other, ModArith))
        assert(self.m == other.m)
        return ModArith(self.val+other.val, self.m)

    def __sub__(self, other):
        assert(isinstance(other, ModArith))
        assert(self.m == other.m)
        return ModArith(self.m+self.val-other.val, self.m)

    def __mul__(self, other):
        assert(isinstance(other, ModArith))
        assert(self.m == other.m)
        return ModArith(self.val*other.val, self.m)

    def __divmod__(self, other):
        assert(isinstance(other, ModArith))
        assert(self.m == other.m)
        quot, rem = 0, self.val
        while rem >= other.val:
            rem = rem - other.val
            quot = quot+1
        return (ModArith(quot, self.m), ModArith(rem, self.m))

    def __eq__(self, other):
        assert(isinstance(other, ModArith))
        assert(self.m == other.m)
        return self.val == other.val

    def __neg__(self):
        return ModArith(self.m-self.val, self.m)

    def iszero(self):
        return self.val == 0

    def __repr__(self):
        return f"{self.val}"

    def zero(self):
        return ModArith(0, self.m)

    def inv(self):
        return ModArith(mod_inverse(self.val, self.m), self.m)


import itertools

def add_(a, b):
    if a is None: return b
    if b is None: return a
    return a+b

def sub_(a, b):
    if a is None: return -b
    if b is None: return a
    return a-b

class Poly:
    def __init__(self, c, ctor):
        self.ctor = ctor
        self.c = [ctor(i) for i in c]
        if len(self.c) > 0:
            while len(self.c) and self.c[0].iszero():
                self.c.pop(0)
            if len(self.c) > 0:
                self.order=len(self.c)-1
            else:
                self.order=0
        else:
            self.order=0

    def scale(self, x):
        return Poly([c*x for c in self.c], self.ctor)

    def __add__(self, other):
        cs = list(add_(a,b) for a, b in itertools.zip_longest(reversed(self.c), reversed(other.c)))
        return Poly(list(reversed(cs)), self.ctor)

    def __sub__(self, other):
        cs = list(sub_(a,b) for a, b in itertools.zip_longest(reversed(self.c), reversed(other.c)))
        return Poly(list(reversed(cs)), self.ctor)

    def __mul__(self, other):
        acc = Poly([], self.ctor)
        x = self
        for c in reversed(other.c):
            acc = acc + x.scale(c)
            x = Poly(x.c+[c.zero()], self.ctor)
        return acc

    def __mod__(self, other):
        return divmod(self, other)[1]

    def __neg__(self):
        return Poly([-c for c in self.c], self.ctor)

    def __divmod__(self, other):
        rem = self
        quot = Poly([], self.ctor)
        while len(rem.c) >= len(other.c):
            r = rem.c[0]
            o = other.c[0]
            order = len(rem.c) - len(other.c)
            c = r * o.inv()
            q = Poly([c]+order*[self.ctor(0)], self.ctor)
            quot = quot + q
            rem = rem - q*other
        return (quot, rem)

    def __repr__(self):
        if len(self.c) == 0: return "0"
        return ' + '.join(reversed([f"{c} x^{n}" if n > 0 else f"{c}" for n, c in enumerate(reversed(self.c))]))

M = lambda x: ModArith(x, 7)
P = lambda x: Poly(list(map(M, x)), M)

a = P([1,2,1,0])
b = P([0,2,0,0])
str(a)
str(b)
str(divmod(a,b))

# In[0]

from hamming2 import allVectors
import numpy as np

def cycCode(gc, k, base):
    M = lambda x: ModArith(x, base)
    P = lambda x: Poly(x, M)
    g = P(gc)
    r = g.order
    n = k+r
    xr = P([1]+r*[0])

    def encode(m):
        z = P(m)*xr
        z = z - (z % g)
        cs = [c.val for c in z.c]
        while len(cs) < n:
            cs.insert(0, 0)
        return cs

    d = min(np.count_nonzero([i for i in encode(m)]) for m in itertools.islice(allVectors(k, base), 1, None))
    ec = (d-1)//2
    print(f"Code distance is {d}, can correct {ec} errors")

    tbl = {}
    for ei in allVectors(n, base):
        if 0 < np.count_nonzero(ei) <= ec:
            si = P(ei) % g
            tbl[str(si)] = np.reshape(ei, n)
    print(f"Table size is {len(tbl)}")

    def decode(c):
        s = P(c) % g
        if all(c.iszero() for c in s.c):
            return c[:k]
        e = tbl[str(s)]
        c1 = c - e
        return c1[:k]

    return (encode, decode)

encode, decode = cycCode(gc=[1,0,1,0,0,1,1,1], k=4, base=4)

# In[0]

c = encode([1,2,3,0])
c[3] += 2
c[5] += 2
decode(c)
