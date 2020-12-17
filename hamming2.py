# код (n, k) n -- символов в код. слове, k -- символов в сообщении
# пор. мат. G размера k×n
# пров. мат. H размер (n-k)×n
G = [
    [1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
] # (7, 4)

import numpy as np

G = np.array(G)
print(G.T)

# In[0]
H = np.array([
    [1, 1, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1],
])

# H×G(T) = 0 (mod q)

np.matmul(H,G.T) % 2

# In[0]

def getH(G, p=2):
    k, n = G.shape
    H = np.zeros(shape=(n-k, n))
    for i in range(k, n):
        H[i-k, i] = 1
    for i in range(k):
        for j in range(k, n):
            H[j-k, i] = p - G[i, j]
    return H

# In[0]

import itertools

def allVectors(len, base=2):
    return (np.array(i) for i in itertools.product(range(base), repeat=len))

# In[0]

def lincode(G, p=2):
    k,n = G.shape

    def encode(m):
        return np.reshape(np.matmul(G.T, np.reshape(np.array(m), (k, 1))) % p, n)

    d = min(np.count_nonzero(encode(m)) for m in itertools.islice(allVectors(k, p), 1, None))
    ec = (d-1)//2
    print(f"Code distance is {d}, can correct {ec} errors")

    H = getH(G, p)
    tbl = {}
    for ei in allVectors(n, p):
        if 0 < np.count_nonzero(ei) <= ec:
            si = np.reshape(np.matmul(H, ei) % p, n-k)
            tbl[str(si)] = np.reshape(ei, n)

    def decode(c):
        s = np.reshape(np.matmul(H, c) % p, n-k)
        if np.count_nonzero(s) == 0:
            return c[:k]
        e = tbl[str(s)]
        c1 = c - e
        return c1[:k]

    return (encode, decode)


encode, decode = lincode(G = np.array([
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 0, 1, 1, 0, 1, 1],
    [0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
]), p=4) # (10, 5)
decode(encode([2,0,3,0,0])+np.array([2,0,0,0,0,0,0,0,0,0]))
