def inv(m, a):
    # a < m
    r0 = m
    r1 = a
    t0 = 0
    t1 = 1
    while r1 > 0:
        rt = r1
        tt = t1
        q = r0//r1
        r1 = r0 - r1*q
        t1 = (t0 - t1*q) % m
        r0 = rt
        t0 = tt
    return t0

# for i in range(1, 17):
#     assert((i*inv(17, i)) % 17 == 1)

# In[0]

def icg(m, a, c, s0):
    s = s0
    while True:
        s = (a*inv(m, s)+c) % m
        yield s

g = icg(11, 5, 3, 3)

list(zip(range(1, 11), g))
