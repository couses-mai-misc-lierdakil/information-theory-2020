import math

def numbytes(l):
    return math.ceil(math.log2(l)/8)

def _encode(s):
    dict = { x.to_bytes(1, 'big'): x for x in range(256) }
    l = len(s)
    i = 1
    start = 0
    while True:
        pfx = s[start:i]
        if pfx not in dict:
            yield dict[pfx[:-1]].to_bytes(numbytes(len(dict)), 'big')
            dict[pfx] = len(dict)
            start = i - 1
        elif i >= l:
            yield dict[pfx].to_bytes(numbytes(len(dict)), 'big')
            break
        else:
            i+=1

def encode(s):
    return b''.join(_encode(bytes(s, 'utf-8')))

def _decode(s):
    dict = [ x.to_bytes(1, 'big') for x in range(256) ]
    def take():
        i = 0
        while i < len(s):
            l1 = numbytes(len(dict))
            l2 = numbytes(len(dict)+1)
            b1 = int.from_bytes(s[i:i+l1], 'big')
            b2 = int.from_bytes(s[i+l1:i+l1+l2], 'big')
            yield (b1, b2)
            i += l1

    for i, j in take():
        c1 = dict[i]
        c2 = dict[j] if j < len(dict) else c1
        dict.append(c1+c2[:1])
        yield c1

def decode(s):
    return str(b''.join(_decode(s)), 'utf-8')

decode(encode('aaaa'))

for n in range(1,1000):
    s = ''.join('a' for i in range(n))
    l = len(encode(s))
    print(n, l/n)
