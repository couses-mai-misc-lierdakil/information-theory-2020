def gen(s0):
    s = s0
    while True:
        s = (10*s + 13) % 16
        yield s

g = gen(1)
for i in range(16):
    print(next(g))

# In[0]

def nextRand(a, c, m, curState):
    return (a*curState + c) % m

s0 = 4

# In[0]

s0 = nextRand(3, 5, 17, s0)
s0
