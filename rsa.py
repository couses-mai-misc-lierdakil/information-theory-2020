p = 227
q = 103

m = p * q

m

# In[0]

φ = (p-1)*(q-1)
φ

# In[0]

e = 257

for d in range(1, φ):
    if d*e % φ == 1:
        break
d

# In[0]

pubkey = (e, m)
privkey = (d, m)

# In[0]

from blom import modpow

s = b'hello, world'

enc = b''.join(modpow(m, b, e).to_bytes(2,'big') for b in s)
enc

dec = b''.join(modpow(m, int.from_bytes(enc[i:i+2], 'big'), d).to_bytes(1,'big') for i in range(0,len(enc),2))
dec

# In[0]
# Криптоанализ

e, m, enc

#m = p*q
#d = e**(-1) % (p-1)(q-1)

# In[0]

from math import sqrt

for i in range(2, round(sqrt(m))):
    if (m//i)*i == m:
        break

# In[0]

j = m // i
γ = (i-1)*(j-1)

for h in range(1, γ):
    if h*e % γ == 1:
        break
h

dec = b''.join(modpow(m, int.from_bytes(enc[i:i+2], 'big'), h).to_bytes(1,'big') for i in range(0,len(enc),2))
dec
