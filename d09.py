# ### Part 1
# out = ''
# with open('d09.txt') as f:
#     while True:
#         c = f.read(1)
#         if not c:
#             break
#
#         if c == '(':
#             pattern = ''
#             while True:
#                 pattern_char = f.read(1)
#                 if pattern_char == ')':
#                     break
#                 else:
#                     pattern += pattern_char
#
#             length, count = (int(n) for n in pattern.split('x'))
#             repstr = f.read(length)
#             out += repstr * count
#
#         else:
#             out += c
#
# print(len(out), end='\n\n')

from collections import deque


def get_cmpstr_len(comp_seq):
    if not comp_seq:
        return 0

    if comp_seq[0] == '(':

        comp_seq.popleft()
        pattern = ''
        while True:
            pattern_char = comp_seq.popleft()
            if pattern_char == ')':
                break
            else:
                pattern += pattern_char

        length, count = (int(n) for n in pattern.split('x'))
        rep_seq = deque(comp_seq.popleft() for _ in range(length))
        return count * get_cmpstr_len(rep_seq) + get_cmpstr_len(comp_seq)

    else:
        comp_seq.popleft()
        return 1 + get_cmpstr_len(comp_seq)



d = deque('(3x3)XYZ')
assert get_cmpstr_len(d) == len('XYZXYZXYZ')

d = deque('X(8x2)(3x3)ABCY')
assert get_cmpstr_len(d) == len('XABCABCABCABCABCABCY')

d = deque('(27x12)(20x12)(13x14)(7x10)(1x12)A')
assert get_cmpstr_len(d) == 241920

d = deque('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN')
assert get_cmpstr_len(d) == 445


with open('d09.txt') as f:
    d = deque(f.read())

print(get_cmpstr_len(d))
