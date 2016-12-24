from collections import defaultdict

import numpy as np

sample_input = ('###########\n'
                '#0.1.....2#\n'
                '#.#######.#\n'
                '#4.......3#\n'
                '###########').splitlines()

with open('d24.txt') as f:
    puzzle_input = f.read().splitlines()

maze_list = []
for line in puzzle_input:
    line_list = []
    for char in line:
        if char == '#':
            line_list.append(-9)
        elif char == '.':
            line_list.append(-1)
        else:
            line_list.append(int(char))
    maze_list.append(line_list)

maze = np.array(maze_list)
points_of_interest = frozenset(zip(*np.where(maze > 0)))
solution_families = defaultdict(set)
starting_location = next(zip(*np.where(maze == 0)))
path = [starting_location]

solutions = [[starting_location, path, path, points_of_interest], ]

i = 0
while solutions:
    new_sol = []
    for curr_coord, recent_path, full_path, remaining_poi in solutions:
        for direc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_coord = tuple(a + b for a, b in zip(curr_coord, direc))
            if maze[next_coord[0], next_coord[1]] >= -1 and (
                    next_coord in remaining_poi or next_coord not in recent_path):

                if next_coord in remaining_poi:
                    new_recent_path = []
                else:
                    new_recent_path = recent_path.copy()
                    new_recent_path.append(next_coord)

                new_poi = remaining_poi - {next_coord}
                new_full_path = full_path.copy()
                new_full_path.append(next_coord)

                if len(new_poi) == 0:
                    if next_coord == starting_location:
                        print('*** Made it back to the starting position in {:02d} steps. ***'.format(
                            len(new_full_path) - 1))
                    else:
                        print(' *  Found all the POI\'s in {:02d} steps.  * '.format(len(new_full_path) - 1))
                        new_poi = frozenset({starting_location})
                        new_sol.append([next_coord, new_recent_path, new_full_path, new_poi])
                elif next_coord not in solution_families[new_poi]:
                    solution_families[new_poi].add(next_coord)
                    new_sol.append([next_coord, new_recent_path, new_full_path, new_poi])

    solutions = new_sol

    i += 1
    if i % 25 == 0:
        print('    Iteration: {:>3}, branches: {:>4}'.format(i, len(solutions)))

print()
