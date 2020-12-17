def _encode(s):
    dict = { '': 0 }
    i = 0
    for l in range(1, len(s)+1):
        pfx = s[i:l]
        if pfx not in dict:
            yield (dict[pfx[:-1]], pfx[-1:])
            dict[pfx] = len(dict)
            i = l
            pfx = ''
    if len(pfx) > 0:
        yield (dict[pfx[:-1]], pfx[-1:])

def binstr(n, l):
    nb = (l-1)//8 + 1
    bytestr = n.to_bytes(nb, 'big')
    bitstr = ''.join(f"{c:08b}" for c in bytestr)
    return bitstr[-l:]

import math

def encode(s):
    return ''.join(binstr(i, math.ceil(math.log2(n+1)))+sf for n, (i, sf) in enumerate(_encode(s)))

def _decode(s):
    dict = ['']
    i = 0
    while i < len(s):
        next = i + 1 + math.ceil(math.log2(len(dict)))
        c = s[i:next]
        pfx = c[:-1]
        sfx = c[-1:]
        ipfx = int(pfx, 2) if len(pfx) > 0 else 0
        x = dict[ipfx] + sfx
        dict.append(x)
        yield x
        i = next

def decode(s):
    return ''.join(_decode(s))

s = '000000000001000000000000'
r = '0101001100011100011000000'

encode('hello')
