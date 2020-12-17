from dh import safePrimes, getG, chooseA, computeA
import math

plen = 1
p = None
for i in safePrimes:
    if math.log2(i)/8 >= plen:
        break
    p = i
p

# In[0]

g = getG(p)
dh=(g, p)
dh

# In[0]

strings = [
  "перенести",
  "плавленый",
  "объездной",
  "отзвенеть",
  "отбивание",
  "грустнеть",
  "поворчать",
  "экскреция",
  "безвинный",
  "ворковать",
  "шишковник",
  "греховный",
  "гречишник",
  "самотёком",
  "турнирный",
  "прогорать",
  "отказчица",
  "шатировка",
  "наглазный",
  "дорваться",
  "натравщик",
  "выдержать",
  "очертание",
  "котельный",
  "пословный",
  "облачение",
  "обшастать",
  "штакетник",
  "латуковый",
  "наспаться"
  ]

import socket
import sys
import random

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 64849)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

try:
    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()

        print('connection from', client_address)

        # connection.sendall(plen.to_bytes(4, byteorder='big'))
        connection.sendall(g.to_bytes(plen, byteorder='big'))
        connection.sendall(p.to_bytes(plen, byteorder='big'))
        a = chooseA(dh)
        A = computeA(dh, a)
        connection.sendall(A.to_bytes(plen, byteorder='big'))
        B = int.from_bytes(connection.recv(plen), byteorder='big')
        if B in ([0] + [g**i % p for i in range((p-1)//2)]):
            connection.close()
            continue
        k = B**a % p

        string = random.choice(strings)
        bstr = bytes(string, 'utf8')
        enc = b''
        for i in range(0, len(bstr), plen):
            blk = int.from_bytes(bstr[i:i+plen], 'big')
            enc += (blk ^ k).to_bytes(plen,'big')
            # k = blk # for anemic streaming cypher
        connection.sendall(enc)
        connection.close()

finally:
    sock.close()
