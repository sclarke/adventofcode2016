import hashlib
from itertools import chain

import attr
from attr.validators import instance_of


@attr.s
class Path(object):
    x = attr.ib(validator=instance_of(int))
    y = attr.ib(validator=instance_of(int))
    h = attr.ib()
    s = attr.ib(default=b'')

    def __add__(self, other):  # coords range from 0 to 3
        def add_saturated(i, j):
            c = i + j
            return i if c > 3 or c < 0 else c

        return Path(
            add_saturated(self.x, other.x),
            add_saturated(self.y, other.y),
        )

    @property
    def available_moves(self):
        open_doors = {direction for char, direction in zip(self.h.hexdigest()[:4], 'UDLR') if char in 'bcdef'}
        allowed_directions = ({0: set('R'), 1: set('RL'), 2: set('RL'), 3: set('L')}[self.x] |
                              {0: set('D'), 1: set('UD'), 2: set('UD'), 3: set('U')}[self.y])
        return open_doors & allowed_directions

    @property
    def spawn_next(self):
        moves = dict(
            U=(b'U', 0, -1),
            D=(b'D', 0, 1),
            L=(b'L', -1, 0),
            R=(b'R', 1, 0),
        )

        children = []
        for move in self.available_moves:
            direc, dx, dy = moves[move]
            new_hash = self.h.copy()
            new_hash.update(direc)
            children.append(Path(self.x + dx, self.y + dy, new_hash, self.s + direc))
        return children


# passcode = b'hijkl'
# passcode = b'ihgpwlah'
# passcode = b'ulqzkmiv'
# passcode = b'ihgpwlah'
# passcode = b'kglvqrro'
# passcode = b'ulqzkmiv'
passcode = b'pxxbnzuo'  # My puzzle input

h = hashlib.new('md5', passcode)
initial_position = Path(0, 0, h)

paths = [initial_position]

solutions = []
while paths:
    paths = list(chain.from_iterable(p.spawn_next for p in paths if not p.x == p.y == 3))
    solutions += [p for p in paths if p.x == p.y == 3]

# solutions = sorted(solutions, key=lambda p: len(p.s))  # shouldn't need to sort this; the last one should be longest.
print('Shortest path: {}'.format(solutions[0].s.decode()))
print('Longest path: {}'.format(len(solutions[-1].s)))
print('\n')
