from dh import choosea, computeA
from blom import modpow
import socket

server_address = ('localhost', 64849)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)

try:
    plen = 1
    g = int.from_bytes(sock.recv(plen), 'big')
    p = int.from_bytes(sock.recv(plen), 'big')
    B = int.from_bytes(sock.recv(plen), 'big')
    dh=(g, p)
    a = choosea(dh)
    A = computeA(dh, a)
    sock.send(A.to_bytes(plen, 'big'))
    k = modpow(p, B, a)
    s = bytes()
    e = bytes()
    while True:
        bs = sock.recv(plen)
        e += bs
        if len(bs) < plen: break
        ord = int.from_bytes(bs, 'big')
        dec = ord ^ k
        s += dec.to_bytes(plen, 'big')

    print(e)
    print(str(s,'utf8'))

finally:
    sock.close()

# In[0]

(g, p, A, B)

for i in range(1, p-1):
    if modpow(p, g, i) == A:
        break
i, a

k = modpow(p, B, i)
str(bytes(c ^ k for c in e), 'utf8')
