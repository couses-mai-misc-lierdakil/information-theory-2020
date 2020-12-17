safePrimes = None
with open('../safe.dat') as f:
    safePrimes = [int(line.split(' ')[1]) for line in f]

from blom import modpow

def isPrim(g, p):
    for n in [2, (p-1)//2]:
        if modpow(p,g,n)==1: return False
    return True

def getG(p):
    return next(g for g in range(2, p) if isPrim(g, p))

[getG(p) for p in safePrimes]

# In[0]

p = 983
g = getG(p)
dh = (g,p)
dh

# In[0]

import random
import math


def choosea(dh):
    g,p = dh
    φ = p - 1
    return random.randint(φ//2, φ-1)

a = choosea(dh)
a

# In[0]

def computeA(dh, a):
    g, p = dh
    return modpow(p, g, a)

A = computeA(dh, a)
A

# In[0]

b = choosea(dh)
B = computeA(dh, b)
b, B

# In[0]

k1 = modpow(p, B, a)
k2 = modpow(p, A, b)
assert(k1 == k2)
k1, k2

# In[0]

dh
computeA(dh, 10)
