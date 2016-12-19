from collections import deque
from math import ceil, floor, log2, log

# part 1
# Standard Josephus Problem has solution f(n) = 2(n - 2**floor(log2(n))) + 1
# https://en.wikipedia.org/wiki/Josephus_problem
# https://www.youtube.com/watch?v=uCsD3ZGzMgE

puzzle_input = 3014603
print(2 * (puzzle_input - 2**floor(log2(puzzle_input))) + 1)


# part 2
# exploring solution space
solutions = {}
for i in range(2, 500):
    elves = deque(range(1, 1 + i))
    while True:
        elves.rotate(ceil(len(elves)/2))
        elves.popleft()
        elves.rotate(ceil(len(elves)/2) - 1)
        if len(elves) == 1:
            sol = (i, elves.pop())
            # print(sol)
            solutions.update([sol,])
            break


# It looks like it resets at 3**m, and then counts by 1 for m/2 and by 2 for m/2
# so the solution should have this: (n-3**floor(log3(n)))


def modified_josephus(n):
    m = 3**floor(log(n, 3))

    l = n-m
    if l == 0:
        return m  # for 3, 9, 27, 81, etc: corner case
    elif l < m:
        return l  # the solutions count 1-by-1 from the last l==0 solution
    else:
        return m + 2*(l-m)  # then they count by two until the next l==0 case

for i in range(2, 500):
    assert solutions[i] == modified_josephus(i)


# So, the part two solution:

print(modified_josephus(puzzle_input), end='\n\n')
