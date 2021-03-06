from collections import defaultdict
from copy import copy
from functools import lru_cache
from itertools import combinations, chain
from re import compile

import attr

generator_pattern = compile(r'(\w+) generator')
microchip_pattern = compile(r'(\w+)-compatible microchip')

floors = []

with open('d11_test.txt') as fh:
    for line in fh:
        generators = (match.lower() for match in generator_pattern.findall(line))
        microchips = (match.upper() for match in microchip_pattern.findall(line))
        floors.append(tuple(sorted(chain(generators, microchips))))


@lru_cache(maxsize=8)
def is_floor_allowed(f):
    return f in range(1, 5)


@attr.s
class Elevator(object):
    location = attr.ib()

    @lru_cache(maxsize=2**10)
    def next_floor(self):
        return {f for f in [self.location + 1, self.location - 1] if is_floor_allowed(f)}


@lru_cache(maxsize=2**20)
def configuration_valid(floor_set):
    for microchip in (device for device in floor_set if device.isupper()):
        if not microchip.lower() in floor_set and [device for device in floor_set if device.islower()]:
            return False
    return True


@lru_cache(maxsize=2**20)
def configuration_signature(floor_set):
    """Calculates a signature for a given configuration.

    Generates the same signature for `similar` configurations (one generator/microchip pair is swapped with another).
    """

    generators_ordered = [device for floor in floor_set for device in floor if device.islower()]

    signature = 0
    for level, floor in enumerate(floor_set):
        for device in floor:
            if device.islower():
                signature += 4 ** generators_ordered.index(device) * level
            else:
                signature += 4 ** (generators_ordered.index(device.lower()) + len(generators_ordered)) * level

    return signature


@lru_cache(maxsize=2**20)
def one_or_two_from(floor_set):
    return list(chain(combinations(floor_set, 1),
                      (combo for combo in combinations(floor_set, 2) if configuration_valid(combo))))


cases = defaultdict(list)

elevator = Elevator(1)
move = 0
cases[move].append((elevator, tuple(floors)))
all_cases = set()
all_cases.add((elevator, configuration_signature(tuple(floors))))

while cases[move]:
    for elevator, floors in cases[move]:

        if not any(floors[:-1]):
            print(move)
            break

        for next_elevator_move in (Elevator(f) for f in elevator.next_floor()):
            for group in one_or_two_from(floors[elevator.location - 1]):

                next_floors = []

                for i, floor in enumerate(floors, 1):
                    if i == next_elevator_move.location:
                        next_floors.append(tuple(sorted(chain(floor, group))))
                    elif i == elevator.location:
                        next_floors.append(tuple(sorted(set(floor) - set(group))))
                    else:
                        next_floors.append(copy(floor))

                if all(configuration_valid(floor) for floor in next_floors):
                    new_case = (next_elevator_move, configuration_signature(tuple(next_floors)))
                    if new_case not in all_cases:
                        cases[move + 1].append((next_elevator_move, tuple(next_floors)))
                        all_cases.add(new_case)

    move += 1
    print('move: {}'.format(move))
