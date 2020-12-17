def unzip(it):
    return tuple(list(i) for i in zip(*it))

def stat(s):
    dict = {}
    for c in s:
        if c in dict:
            dict[c] += 1
        else:
            dict[c] = 1
    return unzip(sorted(dict.items(), key=lambda i: i[1]))

from bisect import bisect

def tree(s):
    stk, stn = stat(s)
    codes = { k: '' for k in stk }
    while len(stk) > 1:
        k1, n1, k2, n2 = stk[0], stn[0], stk[1], stn[1]
        for i in k1:
            codes[i] = '0' + codes[i]
        for i in k2:
            codes[i] = '1' + codes[i]
        stk = stk[2:]
        stn = stn[2:]
        n3 = n1+n2
        i = bisect(stn, n3)
        stk.insert(i, k1+k2)
        stn.insert(i, n3)
    return codes

def encode(s):
    d = tree(s)
    return (d, ''.join(d[c] for c in s))

def _decode(d, s):
    i = 0
    rd = {v: k for k,v in d.items()}
    for l in range(len(s)+1):
        p = s[i:l]
        if p in rd:
            yield rd[p]
            i = l

def decode(d, s):
    return ''.join(_decode(d,s))

decode(*encode("hello, hello"))
