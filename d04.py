import re
from collections import Counter
from itertools import repeat

import attr

with open('d04.txt') as f:
    rooms_raw = f.readlines()

exp = re.compile(r'([a-z-]+)-(\d+)\[([a-z]{5})\]')


@attr.s
class Room(object):
    enc_name = attr.ib()
    sec_id = attr.ib(convert=int)
    chksum = attr.ib()


rooms = [Room(*exp.match(room).groups()) for room in rooms_raw]


def calc_chk(enc_str):
    letters = Counter(enc_str.replace('-', ''))
    sort_letters = sorted(letters.most_common(), key=lambda x: (-x[1], x[0]))
    return ''.join(l[0] for l in sort_letters[:5])


valid_sec_ids = [room.sec_id for room in rooms if room.chksum == calc_chk(room.enc_name)]
print(sum(valid_sec_ids))


def shift_letter(l, n):
    if l == '-': return ' '
    return chr((ord(l) - ord('a') + n) % 26 + ord('a'))


for room in rooms:
    dec_name = ''.join(map(shift_letter, room.enc_name, repeat(room.sec_id)))
    if 'north' in dec_name:
        print(room.sec_id, dec_name)
