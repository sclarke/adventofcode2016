from functools import lru_cache
from hashlib import md5
from itertools import product

salt = b'qzyelonm'
lookahead_distance = 1000


def get_hex_digest(b):
    return md5(b).hexdigest()


def first_repeat_char(hash_str, l=3):
    matches = sorted((hash_str.find(c*l), c) for c in set(hash_str) if c*l in hash_str)
    return matches[0][1] if matches else []


@lru_cache(maxsize=lookahead_distance)
def hash_bytes(b, n):
    return b + str(n).encode()


@lru_cache(maxsize=lookahead_distance)
def get_iter_hex_digest(b, iterations=0):
    for _ in range(iterations+1):
        b = get_hex_digest(b).encode()
    return b.decode()


i = 0
keys = []
key_stretch_rounds = 2016  # part 1: 0; part 2: 2016

while len(keys) < 64:
    digest = get_iter_hex_digest(hash_bytes(salt, i), key_stretch_rounds)
    if any((index, char) for index, char in product(range(i+1, i+1+lookahead_distance), first_repeat_char(digest))
           if char*5 in get_iter_hex_digest(hash_bytes(salt, index), key_stretch_rounds)):
        print(len(keys), i)
        keys.append(i)
    i += 1

print('\n\n', keys[-1], '\n\n')
