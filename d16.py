def dragon_step(a):
    b = [1 - x for x in reversed(a)]
    return a + [0, ] + b


def grouper(iterable, n):
    """Collect data into fixed-length chunks or blocks"""
    args = [iter(iterable)] * n
    return zip(*args)


def checksum(seq):
    if len(seq) % 2:
        return seq
    else:
        return checksum([int(a == b) for a, b in grouper(seq, 2)])


def list_as_str(l):
    return ''.join(str(x) for x in l)


def fill_disk(data, target_size):
    while len(data) < target_size:
        data = dragon_step(data)

    data = data[:target_size]
    return data, checksum(data)


assert list_as_str(dragon_step([1, ])) == '100'
assert list_as_str(dragon_step([0, ])) == '001'
assert list_as_str(dragon_step([int(x) for x in '11111'])) == '11111000000'
assert list_as_str(dragon_step([int(x) for x in '111100001010'])) == '1111000010100101011110000'

assert list_as_str(checksum([int(x) for x in '110010110100'])) == '100'


test_input = '10000'
fill_data, chksum = fill_disk([int(x) for x in test_input], 20)
print('Sample Data: ', *(list_as_str(l) for l in [fill_data, chksum]))


raw_input = '11101000110010100'

fill_data, chksum = fill_disk([int(x) for x in raw_input], 272)
print('Part 1: ', list_as_str(chksum))

fill_data2, chksum2 = fill_disk([int(x) for x in raw_input], 35651584)
print('Part 2: ', list_as_str(chksum2))


print()
