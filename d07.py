import re

with open('d07.txt') as f:
    raw_input = f.readlines()

test_input = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
asdfasdf[qwerqwer]asdffdsa[12341234]zcxvzcv""".splitlines()


def group_finder(s):
    head, _, tail = s.partition('[')
    yield head
    if tail:
        yield from group_finder(tail)


re_abba = re.compile(r'.*([a-z])(?!\1)([a-z])\2\1')

total = 0
for line in raw_input:
    line_groups = list(group_finder(line.replace(']', '[')))
    ips = line_groups[::2]
    hns = line_groups[1::2]
    if any(re_abba.match(ip) for ip in ips) and not any(re_abba.match(hn) for hn in hns):
        total += 1

print(total)

# part 2!

test_input = """aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb""".splitlines()

import regex

re_aba = regex.compile(r'([a-z])(?!\1)([a-z])\1')

total = 0
for line in raw_input:
    line_groups = list(group_finder(line.replace(']', '[')))
    ips = line_groups[::2]
    hns = line_groups[1::2]

    match = False
    for ip in ips:
        for a, b in re_aba.findall(ip, overlapped=True):
            if any(b + a + b in hn for hn in hns):
                match = True

    if match:
        total += 1

print(total)
