# a^x mod p
def modpow(p, a, x):
    if x == 0: return 1
    if x == 1: return a
    r = a
    i = 1 << (x.bit_length() - 2)
    while i > 0:
        r = r * r % p
        if i & x > 0: r = r * a % p
        i = i >> 1
    return r

p = 11
rec = lambda x: modpow(p, x, p-2)

modpow(37, 7, 12)
modpow(37, 33, 12)

# In[0]

import numpy as np

def gauss(a):
    i = 0
    for ii in range(a.shape[0]):
        if a[ii, i] == 0:
            continue

        r = rec(a[ii, i])
        a[ii] = (a[ii] * r) % p
        for j in range(0, a.shape[0]):
            if j == ii: continue
            a[j] = (a[j] - a[j, i] * a[ii]) % p
        if i < a.shape[1]-1:
            i += 1
    return np.array([row for row in a if sum(row) > 0])

gauss(np.array([
    [1, 3, 3, 0, 0, 0, 3],
    [1, 3, 7, 0, 0, 0, 1],
    [3, 5, 1, 0, 0, 0, 1],
    [0, 1, 0, 3, 3, 0, 1],
    [0, 1, 0, 3, 7, 0, 3],
    [0, 3, 0, 5, 1, 0, 0],
    [0, 0, 1, 0, 3, 3, 0],
    [0, 0, 1, 0, 3, 7, 6],
    [0, 0, 3, 0, 5, 1, 8],
]))
