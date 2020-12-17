import math
import subprocess
import random
import sys

# Wrapper for Morain ECPP suite http://www.lix.polytechnique.fr/~morain/Prgms/ecpp.english.html

def checkprime(n):
    with open('/tmp/num.txt', 'w') as f:
        f.write(str(n))
    res = subprocess.run(["/home/livid/Downloads/ECPP-V6.4.5a/xrunecpp", "-f/tmp/num.txt"], capture_output=True)
    return 'This number is prime' in [line for line in str(res.stdout, 'utf-8').split('\n') if len(line) > 0 and not line.startswith('%')]

hasECPP = True
try:
    # basic tests to see if it works
    assert(checkprime(115792082982608568644622552645940407664715668381823058010044768391875551821823))
    assert(not checkprime(115792082982608575976279462813722249741598289126422956504981836619222590951079))
except:
    print('Morain ECPP not found or not functional')
    hasECPP = False

# In[0]

def modpow(p, a, x):
    if x==0: return 1
    if x==1: return a
    r = a
    i = 1 << (x.bit_length()-2)
    while i > 0:
        r = r * r % p
        if i & x > 0: r = r * a % p
        i = i >> 1
    return r

def millerRabin(ε, n):
    if n == 2: return True
    if n & 1 == 0: return False
    # вероятность ошибки ε = 2**(-2*k) ⇒ -log2(ε)/2 = k
    k = min(n-1, math.ceil(-math.log2(ε)/2))
    # n-1 == 2**s * d
    d = n-1
    s = 0
    while d & 1 == 0:
        d = d >> 1
        s += 1
    # Для простого n:
    # ∀ a < n:
    # a**d == 1 (mod n) ИЛИ ∃ r < s: a**(2**r*d) == n-1 (mod n)
    # Обратно, для составного n:
    # ∃ a < n:
    # a**d != 1 (mod n) И ∀ r < s: a**(2**r*d) != n-1 (mod n)
    if n < sys.maxsize:
        aas = random.sample(range(1, n), k=k)
    else:
        # для больших чисел вероятно достаточно aas = (random.randrange(1,n) for i in range(k))
        # т.к. вероятность получить дубликаты мала
        aas = set()
        while len(aas) < k:
            aas.add(random.randrange(1,n))
    for a in aas:
        apowd = modpow(n, a, d)
        if (modpow(n, a, d) != 1) and all(modpow(n, apowd, 1 << r) != n-1 for r in range(0, s)):
            return False
    return True

if hasECPP:
    # Test millerRabin for first 300 primes
    i = 2
    n = 0
    while n < 300:
        isPrime = checkprime(i)
        assert(millerRabin(1e-10, i) == isPrime)
        if isPrime: n+=1
        i+=1

# In[0]

# INPUTS
bits = 32
state_size = 8

# DERIVED
b = 2**bits
r = state_size - 1
a = b-1

ε = 1e-23 # probably overkill
while a>1:
    p = a*b**r - 1
    if millerRabin(ε, p):
        halfp = (p-1)//2
        if millerRabin(ε, halfp):
            print(f'a={a}')
            print(f'p={p}')
            λ = a*b**r//2 - 1
            print(f'λ={λ}=2^{math.log2(λ)}')
            break
    a = a-1
