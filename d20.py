
with open('d20.txt') as f:
    raw_input = f.readlines()

# Part 1
blocked = sorted((int(start), int(end)) for (start, end) in [line.split('-') for line in raw_input])

i = 0
for start, end in blocked:
    if i >= start:
        i = max(i, end + 1)

print(i)


# Part 2
blocked_unioned = [blocked[0], ]  # initializing the new list with the first item to avoid the first case being weird
for new_start, new_end in blocked:
    old_start, old_end = blocked_unioned[-1]
    if old_start <= new_start < old_end:
        blocked_unioned[-1] = (old_start, max(new_end, old_end))
    else:
        blocked_unioned.append((new_start, new_end))

blocked_count = sum(end+1 - start for start, end in blocked_unioned)
print(2**32 - blocked_count)
