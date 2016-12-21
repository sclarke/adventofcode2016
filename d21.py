from collections import deque
import re
from copy import copy

test_input = list('abcde')

test_scramble = """swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d""".splitlines()


swap_pos = re.compile(r'swap position (?P<pos1>\d+) with position (?P<pos2>\d+)', re.IGNORECASE)
swap_let = re.compile(r'swap letter (?P<let1>\w) with letter (?P<let2>\w)', re.IGNORECASE)
rotate_dir = re.compile(r'rotate (?P<direction>left|right) (?P<distance>\d+) steps?', re.IGNORECASE)
rotate_indir = re.compile(r'rotate based on position of letter (?P<letter>\w)', re.IGNORECASE)
reverse_pos = re.compile(r'reverse positions (?P<pos1>\d+) through (?P<pos2>\d+)', re.IGNORECASE)
move_pos = re.compile(r'move position (?P<pos1>\d+) to position (?P<pos2>\d+)', re.IGNORECASE)


def f_swap_pos(s, p1, p2, reverse=False):
    seq = copy(s)
    x, y = s[int(p1)], s[int(p2)]
    seq[int(p1)], seq[int(p2)] = y, x
    return seq


def f_swap_let(s, l1, l2, reverse=False):
    seq = copy(s)
    p1, p2 = s.index(l1), s.index(l2)
    seq[p1], seq[p2] = l2, l1
    return seq


def f_rotate_dir(s, direc, dist, reverse=False):
    seq = deque(s)
    d = {'left': -1, 'right': 1}
    if reverse:
        d = {k: -1*v for k, v in d.items()}
    seq.rotate(d[direc] * int(dist))
    return list(seq)


def f_rotate_indir(s, letter, reverse=False):
    seq = deque(s)
    ind = s.index(letter)
    if reverse:
        ind = {
            0: -1,
            1: -1,
            2: -6,
            3: -2,
            4: -7,
            5: -3,
            6: -0,
            7: -4,
        }[ind]
    else:
        if ind >= 4:
            ind += 1
        ind += 1

    seq.rotate(ind)
    return list(seq)


def f_reverse_pos(s, p1, p2, reverse=False):
    seq = copy(s)
    return seq[:int(p1)] + seq[int(p1):int(p2)+1][::-1] + seq[int(p2)+1:]


def f_move_pos(s, p1, p2, reverse=False):
    seq = copy(s)
    if reverse:
        p1, p2 = p2, p1
    letter = seq.pop(int(p1))
    seq.insert(int(p2), letter)
    return seq

commands = {
    swap_pos: f_swap_pos,
    swap_let: f_swap_let,
    rotate_dir: f_rotate_dir,
    rotate_indir: f_rotate_indir,
    reverse_pos: f_reverse_pos,
    move_pos: f_move_pos,
}


test_seq = test_input
for line in test_scramble:
    for regex, func in commands.items():
        m = regex.match(line)
        if m:
            test_seq = func(test_seq, *m.groups())

print('\nTest secuence yields {}\n\n'.format(''.join(test_seq)))


with open('d21.txt') as f:
    real_scramble = f.readlines()

real_input = list('abcdefgh')

reverse = True  # for part 2
if reverse:
    real_scramble = reversed(real_scramble)
    real_input = list('fbgdceah')


working_seq = real_input
print('', ''.join(working_seq))
for line in real_scramble:
    for regex, func in commands.items():
        m = regex.match(line)
        if m:
            working_seq = func(working_seq, *m.groups(), reverse=reverse)
            print(line, ''.join(working_seq))


print('\nReal code yields {}\n\n'.format(''.join(working_seq)))
