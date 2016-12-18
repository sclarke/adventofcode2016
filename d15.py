import re

import attr

raw_input = '''Disc #1 has 13 positions; at time=0, it is at position 1.
Disc #2 has 19 positions; at time=0, it is at position 10.
Disc #3 has 3 positions; at time=0, it is at position 2.
Disc #4 has 7 positions; at time=0, it is at position 1.
Disc #5 has 5 positions; at time=0, it is at position 3.
Disc #6 has 17 positions; at time=0, it is at position 5.
'''

# raw_input = '''Disc #1 has 5 positions; at time=0, it is at position 4.
# Disc #2 has 2 positions; at time=0, it is at position 1.
# '''

parser = re.compile(r"""Disc .(?P<disk_number>\d+) has (?P<position_count>\d+) positions;"""
                    r""" at time=(?P<reftime>\d+), it is at position (?P<refpos>\d+).""")

struct_input = [parser.match(line).groupdict() for line in raw_input.splitlines()]


@attr.s
class Disk(object):
    disk_number = attr.ib(convert=int)
    position_count = attr.ib(convert=int)
    refpos = attr.ib(convert=int)
    reftime = attr.ib(convert=int)

    def aligned(self, time):
        dt = time - self.reftime + self.disk_number
        return (self.refpos + dt) % self.position_count == 0


disks = [Disk(d['disk_number'], d['position_count'], d['refpos'], d['reftime']) for d in struct_input]

i = 0
while True:
    if all(d.aligned(i) for d in disks):
        print('Success: Round {}'.format(i))
        break
    i += 1
print()


# Part 2:
disks.append(Disk(len(disks)+1, 11, 0, 0))

i = 0
while True:
    if all(d.aligned(i) for d in disks):
        print('Success: Round {}'.format(i))
        break
    i += 1
print()
