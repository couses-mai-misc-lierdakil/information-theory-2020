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

def getH(G):
    k, n = G.shape
    H = np.zeros(shape=(n-k, n))
    for i in range(k, n):
        H[i-k, i] = 1
    for i in range(k):
        for j in range(k, n):
            H[j-k, i] = G[i, j]
    return H

# In[0]

def lincode(G, p=2):
    k,n = G.shape
    H = getH(G)
    tbl = {}
    for i in range(n):
        ei = np.zeros((n, 1))
        ei[i, 0] = 1
        si = np.reshape(np.matmul(H, ei) % p, n-k)
        tbl[str(si)] = np.reshape(ei, n)

    def encode(G, m):
        return np.reshape(np.matmul(G.T, np.reshape(np.array(m), (k, 1))) % p, n)

    def decode(G, c):
        s = np.reshape(np.matmul(H, c) % p, n-k)
        if sum(s) == 0:
            return c[:k]
        e = tbl[str(s)]
        c1 = c - e
        return c1[:k]

    return (encode, decode)


encode, decode = lincode(G = np.array([
    [1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 1],
    [0, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 1, 1, 1, 1],
])) # (7, 4)
decode(G,encode(G, [1,0,1,0])+np.array([0,0,0,1,0,0,0]))
