import numpy as np

from matplotlib import pyplot as plt

with open('d08.txt') as f:
    raw_input = f.readlines()

screen = np.zeros((6, 50))

cmd_seq = [line.strip().partition(' ')[::2] for line in raw_input]


def rect_cmd_decode(s):
    return tuple(int(n) for n in s.split('x'))


def rotate_cmd_decode(s):
    r_or_c, pos, _, offset = s.split(' ')

    axes = {'row': 1, 'column': 0}
    coord = int(pos[2:])
    offset = int(offset)

    return axes[r_or_c], coord, offset


def draw_rect(a, p):
    x, y = rect_cmd_decode(p)
    a[0:y, 0:x] = 1


def draw_rot(a, p):
    axis, coordinate, distance = rotate_cmd_decode(p)

    view = a[coordinate, :] if axis else a[:, coordinate]
    view[:] = np.roll(view, distance, axis=0)


commands = {
    'rect': draw_rect,
    'rotate': draw_rot,
}

for cmd, params in cmd_seq:
    commands[cmd](screen, params)

plt.matshow(screen)
plt.show()

print(screen.sum().astype(np.int), end='\n\n')
