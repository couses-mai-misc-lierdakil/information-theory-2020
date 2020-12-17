def _encode(s):
    dict = { b'': 0 }
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
    return n.to_bytes(nb, 'big')

import math

def encode(s):
    return b''.join(
        binstr(i, math.ceil(math.log2(n+1)))+sf
        for n, (i, sf) in enumerate(_encode(bytes(s, 'utf-8'))))

def _decode(s):
    dict = [b'']
    i = 0
    while i < len(s):
        next = i + 1 + math.ceil(math.log2(len(dict))/8)
        c = s[i:next]
        pfx = c[:-1]
        sfx = c[-1:]
        ipfx = int.from_bytes(pfx, 'big') if len(pfx) > 0 else 0
        x = dict[ipfx] + sfx
        dict.append(x)
        yield x
        i = next

def decode(s):
    return str(b''.join(_decode(s)), 'utf-8')

for n in range(9000,10000):
    inp_len = n
    enc_len = len(encode(''.join('a' for i in range(n))))
    print(inp_len, enc_len, enc_len/inp_len)
