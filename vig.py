import itertools

def vigenere(message, key, alphabet, enc=True):
    alen = len(alphabet)
    ord = lambda x: alphabet.index(x)
    chr = lambda x: alphabet[x]
    s = 1 if enc else -1
    return ''.join(chr((ord(ch) + s*(ord(k) + 1)) % alen) for ch, k in zip(message,itertools.cycle(key)))

a = " абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
#devigenere(vigenere("мир труд май", "абв", a), "абв", a)

vigenere("жбябёхсплуллжбябёофщлзёглулзхьцхю", "дек", a, enc=False)
