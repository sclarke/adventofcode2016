import numpy as np


def is_open(y, x, puzzle_input=1358):
    algebraic_sum = x*x + 3*x + 2*x*y + y + y*y + puzzle_input
    return int('{:b}'.format(algebraic_sum).count('1') % 2 == 0)


def find_neighbors(x, y, _map):
    return {(m, n) for (m, n) in ((x+1, y), (max(x-1, 0), y), (x, y+1), (x, max(y-1,0))) if _map[m][n]}


floor_map = []
for x in range(120):
    column = []
    for y in range(120):
        column.append(is_open(x, y))
    floor_map.append(column)

starting_point = (1, 1)
neighbors = {starting_point,}

n = 200  # semaphore for unreached points
dist_map = np.ones_like(floor_map)
dist_map[:, :] = n
dist_map[starting_point] = 0

i = 1
while neighbors:
    neighbors = {(a, b) for (j, k) in neighbors for (a, b) in find_neighbors(j, k, floor_map) if dist_map[a, b] == n}
    for neighbor in neighbors:
        dist_map[neighbor] = i
    i += 1

print('furthest distance searched: {i:}'.format(i=i))
print('steps to ({A:}, {B:}): {C:}'.format(A=39, B=31, C=dist_map[39, 31]))
print('steps that are <= {N:} away: {S:}'.format(N=50, S=np.sum(dist_map <= 50)))
print()
