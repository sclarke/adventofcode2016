from collections import deque, Counter

command_string = "L2, L3, L3, L4, R1, R2, L3, R3, R3, L1, L3, R2, R3, L3, R4, R3, R3, L1, L4, R4, L2, R5, R1, L5, R1, " \
                 "R3, L5, R2, L2, R2, R1, L1, L3, L3, R4, R5, R4, L1, L189, L2, R2, L5, R5, R45, L3, R4, R77, L1, R1, " \
                 "R194, R2, L5, L3, L2, L1, R5, L3, L3, L5, L5, L5, R2, L1, L2, L3, R2, R5, R4, L2, R3, R5, L2, L2, " \
                 "R3, L3, L2, L1, L3, R5, R4, R3, R2, L1, R2, L5, R4, L5, L4, R4, L2, R5, L3, L2, R4, L1, L2, R2, R3, " \
                 "L2, L5, R1, R1, R3, R4, R1, R2, R4, R5, L3, L5, L3, L3, R5, R4, R1, L3, R1, L3, R3, R3, R3, L1, R3, " \
                 "R4, L5, L3, L1, L5, L4, R4, R1, L4, R3, R3, R5, R4, R3, R3, L1, L2, R1, L4, L4, L3, L4, L3, L5, R2, " \
                 "R4, L2"
commands = command_string.split(sep=', ')
direction = 'N'
directions = deque([('N', (0, 1)), ('E', (1, 0)), ('S', (0, -1)), ('W', (-1, 0))])
position = (0, 0)

orth_totals = Counter()
trail = Counter((position, 1))


def coord_add(*args):
    return tuple(sum(vals) for vals in zip(*args))


for cmd in commands:
    turn, *dist = cmd[0], int(cmd[1:])
    if turn == "R":
        directions.rotate(-1)
    else:
        directions.rotate(1)

    orth_totals[directions[0][0]] += dist

    for i in range(dist):
        if trail.most_common(1)[0][1] > 1:
            continue
        position = coord_add(position, directions[0][1])
        trail[position] += 1

print(abs(orth_totals['N'] - orth_totals['S']) + abs(orth_totals['W'] - orth_totals['E']))
print(trail.most_common(1))
